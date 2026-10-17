[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModRoot,

    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ModRoot).Path
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

function Add-ValidationError([string]$Message) { [void]$script:errors.Add($Message) }
function Add-ValidationWarning([string]$Message) { [void]$script:warnings.Add($Message) }

function Read-BlockNumbers([string]$Text, [string]$Key) {
    $match = [regex]::Match($Text, ("(?s)" + $Key + "\s*=\s*\{(.*?)\}"))
    if (-not $match.Success) { return @() }
    return @([regex]::Matches($match.Groups[1].Value, '\b\d+\b') | ForEach-Object { [int]$_.Value })
}

function Read-FirstInt([string]$Text, [string]$Pattern) {
    $match = [regex]::Match($Text, $Pattern)
    if ($match.Success) { return [int]$match.Groups[1].Value }
    return $null
}

function Read-FirstToken([string]$Text, [string]$Pattern) {
    $match = [regex]::Match($Text, $Pattern)
    if ($match.Success) { return $match.Groups[1].Value }
    return ''
}

function Get-BmpInfo([string]$Path) {
    $bytes = [IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -lt 54 -or $bytes[0] -ne 0x42 -or $bytes[1] -ne 0x4d) {
        Add-ValidationError "Invalid BMP header: $Path"
        return $null
    }
    return [pscustomobject]@{
        File = (Split-Path -Leaf $Path)
        Width = [BitConverter]::ToInt32($bytes, 18)
        Height = [BitConverter]::ToInt32($bytes, 22)
        BitsPerPixel = [BitConverter]::ToInt16($bytes, 28)
        Bytes = $bytes.Length
    }
}

function Assert-File([string]$RelativePath) {
    $path = Join-Path $root ($RelativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-ValidationError "Missing required map file: $RelativePath"
    }
    return $path
}

$definitionPath = Assert-File 'map/definition.csv'
$provinceMapPath = Assert-File 'map/provinces.bmp'
$definitionRows = @(Get-Content -LiteralPath $definitionPath | Where-Object { $_ -and $_ -notmatch '^\s*#' })
$definitions = @(
    foreach ($line in $definitionRows) {
        $parts = $line -split ';'
        if ($parts.Count -lt 8 -or $parts[0] -notmatch '^\d+$') {
            Add-ValidationError "Malformed definition.csv row: $line"
            continue
        }
        [pscustomobject]@{
            Id = [int]$parts[0]
            Kind = $parts[4]
            Terrain = $parts[6]
        }
    }
)
$definitionSet = New-Object System.Collections.Generic.HashSet[int]
foreach ($definition in $definitions) { [void]$definitionSet.Add($definition.Id) }
$duplicateDefinitionIds = @($definitions | Group-Object Id | Where-Object Count -gt 1)
if ($duplicateDefinitionIds.Count -gt 0) { Add-ValidationError "Duplicate province IDs in definition.csv: $($duplicateDefinitionIds.Count)" }

$statePath = Join-Path $root 'history/states'
$stateFiles = @(Get-ChildItem -LiteralPath $statePath -File)
$states = @(
    foreach ($file in $stateFiles) {
        $text = Get-Content -LiteralPath $file.FullName -Raw
        $provinceIds = @(Read-BlockNumbers $text 'provinces')
        [pscustomobject]@{
            File = $file.Name
            Id = Read-FirstInt $text '(?m)^\s*id\s*=\s*(\d+)'
            Owner = Read-FirstToken $text '(?m)^\s*owner\s*=\s*([A-Z0-9_]+)'
            ProvinceIds = $provinceIds
        }
    }
)
$duplicateStateIds = @($states | Group-Object Id | Where-Object Count -gt 1)
if ($duplicateStateIds.Count -gt 0) { Add-ValidationError "Duplicate state IDs: $($duplicateStateIds.Count)" }
$stateProvinceRefs = @($states | ForEach-Object ProvinceIds)
$stateProvinceSet = New-Object System.Collections.Generic.HashSet[int]
foreach ($id in $stateProvinceRefs) { [void]$stateProvinceSet.Add($id) }
$unknownStateProvinceIds = @($stateProvinceRefs | Sort-Object -Unique | Where-Object { -not $definitionSet.Contains($_) })
if ($unknownStateProvinceIds.Count -gt 0) { Add-ValidationError "State files reference unknown province IDs: $($unknownStateProvinceIds.Count)" }
$repeatedStateProvinceIds = @($stateProvinceRefs | Group-Object | Where-Object Count -gt 1)
if ($repeatedStateProvinceIds.Count -gt 0) { Add-ValidationError "Province IDs assigned to multiple states: $($repeatedStateProvinceIds.Count)" }
$unassignedStateDefinitions = @($definitions | Where-Object { $_.Id -gt 0 -and -not $stateProvinceSet.Contains($_.Id) })
$unassignedStateLand = @($unassignedStateDefinitions | Where-Object { $_.Kind -eq 'land' -and $_.Terrain -notin @('lakes', 'lake') })
if ($unassignedStateLand.Count -gt 0) { Add-ValidationError "Non-lake land provinces are not assigned to states: $($unassignedStateLand.Count)" }
$placeholderStates = @($states | Where-Object Owner -eq 'PLH')
if ($placeholderStates.Count -gt 0) { Add-ValidationWarning "Placeholder-owned states remain: $($placeholderStates.Count)" }

$strategicPath = Join-Path $root 'map/strategicregions'
$strategicFiles = @(Get-ChildItem -LiteralPath $strategicPath -File)
$strategic = @(
    foreach ($file in $strategicFiles) {
        $text = Get-Content -LiteralPath $file.FullName -Raw
        [pscustomobject]@{
            File = $file.Name
            Id = Read-FirstInt $text '(?m)^\s*id\s*=\s*(\d+)'
            ProvinceIds = @(Read-BlockNumbers $text 'provinces')
        }
    }
)
$duplicateStrategicIds = @($strategic | Group-Object Id | Where-Object Count -gt 1)
if ($duplicateStrategicIds.Count -gt 0) { Add-ValidationError "Duplicate strategic-region IDs: $($duplicateStrategicIds.Count)" }
$strategicProvinceRefs = @($strategic | ForEach-Object ProvinceIds)
$strategicProvinceSet = New-Object System.Collections.Generic.HashSet[int]
foreach ($id in $strategicProvinceRefs) { [void]$strategicProvinceSet.Add($id) }
$unknownStrategicProvinceIds = @($strategicProvinceRefs | Sort-Object -Unique | Where-Object { -not $definitionSet.Contains($_) })
if ($unknownStrategicProvinceIds.Count -gt 0) { Add-ValidationError "Strategic regions reference unknown province IDs: $($unknownStrategicProvinceIds.Count)" }
$repeatedStrategicProvinceIds = @($strategicProvinceRefs | Group-Object | Where-Object Count -gt 1)
if ($repeatedStrategicProvinceIds.Count -gt 0) { Add-ValidationError "Province IDs assigned to multiple strategic regions: $($repeatedStrategicProvinceIds.Count)" }
$unassignedStrategicDefinitions = @($definitions | Where-Object { $_.Id -gt 0 -and -not $strategicProvinceSet.Contains($_.Id) })
if ($unassignedStrategicDefinitions.Count -gt 0) { Add-ValidationError "Province IDs missing from strategic regions: $($unassignedStrategicDefinitions.Count)" }
$placeholderStrategic = @($strategicFiles | Where-Object { $_.Name -match '-XXX\.txt$|Placeholder' })
if ($placeholderStrategic.Count -gt 0) { Add-ValidationWarning "Placeholder strategic-region files remain: $($placeholderStrategic.Count)" }

$adjacencyPath = Assert-File 'map/adjacencies.csv'
$adjacencyRows = @(Get-Content -LiteralPath $adjacencyPath | Select-Object -Skip 1 | Where-Object { $_ -and $_ -notmatch '^-1;-1' })
$badAdjacencyRows = @()
foreach ($line in $adjacencyRows) {
    $parts = $line -split ';'
    if ($parts.Count -lt 2 -or $parts[0] -notmatch '^\d+$' -or $parts[1] -notmatch '^\d+$' -or -not $definitionSet.Contains([int]$parts[0]) -or -not $definitionSet.Contains([int]$parts[1])) {
        $badAdjacencyRows += $line
    }
}
if ($badAdjacencyRows.Count -gt 0) { Add-ValidationError "Adjacency rows with invalid endpoints: $($badAdjacencyRows.Count)" }

foreach ($relative in @('map/airports.txt', 'map/rocketsites.txt')) {
    $path = Assert-File $relative
    $bad = @()
    foreach ($line in @(Get-Content -LiteralPath $path | Where-Object { $_ -match '^\s*\d+\s*=\s*\{\s*\d+' })) {
        $match = [regex]::Match($line, '\{\s*(\d+)')
        if (-not $match.Success -or -not $definitionSet.Contains([int]$match.Groups[1].Value)) { $bad += $line }
    }
    if ($bad.Count -gt 0) { Add-ValidationError "$relative contains invalid province references: $($bad.Count)" }
}

$buildingsPath = Assert-File 'map/buildings.txt'
$buildingRows = @(Get-Content -LiteralPath $buildingsPath | Where-Object { $_ -match '^\s*\d+;' })
$buildingStateKeys = @($buildingRows | ForEach-Object { [int](($_ -split ';')[0]) } | Sort-Object -Unique)
$missingBuildingStateKeys = @($states | ForEach-Object Id | Where-Object { $buildingStateKeys -notcontains $_ })
if ($missingBuildingStateKeys.Count -gt 0) { Add-ValidationWarning "States without buildings.txt placement keys: $($missingBuildingStateKeys.Count)" }

$positionsPath = Assert-File 'map/positions.txt'
if ((Get-Item -LiteralPath $positionsPath).Length -eq 0) { Add-ValidationWarning 'map/positions.txt is empty; runtime placement/rendering verification is required.' }

$rasterFiles = @('provinces.bmp', 'heightmap.bmp', 'terrain.bmp', 'rivers.bmp', 'trees.bmp', 'cities.bmp', 'world_normal.bmp')
$rasters = @()
foreach ($raster in $rasterFiles) {
    $path = Assert-File ("map/$raster")
    if (Test-Path -LiteralPath $path) { $rasters += Get-BmpInfo $path }
}
$provinceRaster = $rasters | Where-Object File -eq 'provinces.bmp'
if ($provinceRaster -and ($provinceRaster.Width -ne 5632 -or $provinceRaster.Height -ne 2048)) { Add-ValidationWarning "Unexpected provinces.bmp dimensions: $($provinceRaster.Width)x$($provinceRaster.Height)" }

$summary = [ordered]@{
    ModRoot = $root
    DefinitionRows = $definitions.Count
    DefinitionMaxId = ($definitions.Id | Measure-Object -Maximum).Maximum
    LandDefinitions = @($definitions | Where-Object Kind -eq 'land').Count
    SeaDefinitions = @($definitions | Where-Object Kind -eq 'sea').Count
    StateFiles = $states.Count
    PlaceholderOwnedStates = $placeholderStates.Count
    UnassignedStateDefinitions = $unassignedStateDefinitions.Count
    UnassignedNonLakeLandDefinitions = $unassignedStateLand.Count
    StrategicRegionFiles = $strategic.Count
    PlaceholderStrategicRegionFiles = $placeholderStrategic.Count
    StrategicProvinceReferences = $strategicProvinceRefs.Count
    AdjacencyRows = $adjacencyRows.Count
    BuildingPlacementRows = $buildingRows.Count
    BuildingStateKeys = $buildingStateKeys.Count
    EmptyPositionsFile = ((Get-Item -LiteralPath $positionsPath).Length -eq 0)
    Errors = $errors.Count
    Warnings = $warnings.Count
}

if ($Json) {
    [pscustomobject]@{ Summary = $summary; Errors = @($errors); Warnings = @($warnings); Rasters = $rasters } | ConvertTo-Json -Depth 5
} else {
    $summary.GetEnumerator() | ForEach-Object { '{0}={1}' -f $_.Key, $_.Value }
    if ($errors.Count -gt 0) { Write-Output 'ERRORS:'; $errors | ForEach-Object { "- $_" } }
    if ($warnings.Count -gt 0) { Write-Output 'WARNINGS:'; $warnings | ForEach-Object { "- $_" } }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
