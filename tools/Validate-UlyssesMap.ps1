[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModRoot,

    [string]$ReferenceGameRoot,

    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $ModRoot).Path
$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$notes = New-Object System.Collections.Generic.List[string]

function Add-ValidationError([string]$Message) { [void]$script:errors.Add($Message) }
function Add-ValidationWarning([string]$Message) { [void]$script:warnings.Add($Message) }
function Add-ValidationNote([string]$Message) { [void]$script:notes.Add($Message) }

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

function Get-BmpColors([string]$Path) {
    if (-not ('UlyssesBmpReader' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.IO;

public static class UlyssesBmpReader
{
    public static HashSet<int> Read24(string path)
    {
        using (var stream = File.OpenRead(path))
        using (var reader = new BinaryReader(stream))
        {
            if (reader.ReadByte() != 0x42 || reader.ReadByte() != 0x4d)
                throw new InvalidDataException("Not a BMP file.");
            stream.Seek(10, SeekOrigin.Begin);
            int offset = reader.ReadInt32();
            stream.Seek(18, SeekOrigin.Begin);
            int width = reader.ReadInt32();
            int height = reader.ReadInt32();
            stream.Seek(28, SeekOrigin.Begin);
            short bitsPerPixel = reader.ReadInt16();
            if (width <= 0 || height == 0 || bitsPerPixel != 24)
                throw new InvalidDataException("Only non-empty 24-bit BMPs are supported.");
            int absoluteHeight = Math.Abs(height);
            int stride = ((width * 3 + 3) / 4) * 4;
            var colors = new HashSet<int>();
            var row = new byte[stride];
            for (int y = 0; y < absoluteHeight; y++)
            {
                stream.Seek(offset + (long)y * stride, SeekOrigin.Begin);
                int read = stream.Read(row, 0, row.Length);
                if (read != row.Length) throw new InvalidDataException("Truncated BMP pixel data.");
                for (int x = 0; x < width; x++)
                {
                    int index = x * 3;
                    int blue = row[index];
                    int green = row[index + 1];
                    int red = row[index + 2];
                    colors.Add((red << 16) | (green << 8) | blue);
                }
            }
            return colors;
        }
    }
}
'@
    }
    try { return [UlyssesBmpReader]::Read24($Path) }
    catch { Add-ValidationError "Could not inspect BMP colors: $Path ($($_.Exception.Message))"; return $null }
}

function Assert-File([string]$RelativePath) {
    $path = Join-Path $root ($RelativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-ValidationError "Missing required map file: $RelativePath"
    }
    return $path
}

function Try-ReadInvariantDouble([string]$Text, [ref]$Value) {
    $parsed = 0.0
    if ([double]::TryParse($Text, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$parsed)) {
        $Value.Value = $parsed
        return $true
    }
    return $false
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
            Red = [int]$parts[1]
            Green = [int]$parts[2]
            Blue = [int]$parts[3]
            Kind = $parts[4]
            Terrain = $parts[6]
            Color = (([int]$parts[1] -shl 16) -bor ([int]$parts[2] -shl 8) -bor [int]$parts[3])
        }
    }
)
$definitionSet = New-Object System.Collections.Generic.HashSet[int]
foreach ($definition in $definitions) { [void]$definitionSet.Add($definition.Id) }
$duplicateDefinitionIds = @($definitions | Group-Object Id | Where-Object Count -gt 1)
if ($duplicateDefinitionIds.Count -gt 0) { Add-ValidationError "Duplicate province IDs in definition.csv: $($duplicateDefinitionIds.Count)" }
$duplicateDefinitionColors = @($definitions | Group-Object Color | Where-Object Count -gt 1)
if ($duplicateDefinitionColors.Count -gt 0) { Add-ValidationError "Duplicate province RGB colors in definition.csv: $($duplicateDefinitionColors.Count)" }

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
$positionsEmpty = ((Get-Item -LiteralPath $positionsPath).Length -eq 0)
$referencePositionsEmpty = $null
if ($ReferenceGameRoot) {
    $referenceRoot = (Resolve-Path -LiteralPath $ReferenceGameRoot).Path
    $referencePositionsPath = Join-Path $referenceRoot 'map/positions.txt'
    if (Test-Path -LiteralPath $referencePositionsPath -PathType Leaf) {
        $referencePositionsEmpty = ((Get-Item -LiteralPath $referencePositionsPath).Length -eq 0)
        if ($positionsEmpty -and $referencePositionsEmpty) {
            Add-ValidationNote 'map/positions.txt is empty, matching the installed HOI4 reference format; no concrete mismatch was found.'
        } elseif ($positionsEmpty) {
            Add-ValidationWarning 'map/positions.txt is empty while the installed reference contains placement data; runtime placement/rendering verification is required.'
        }
    } else {
        Add-ValidationWarning 'ReferenceGameRoot was supplied but map/positions.txt was not found beneath it.'
    }
} elseif ($positionsEmpty) {
    Add-ValidationWarning 'map/positions.txt is empty; pass -ReferenceGameRoot to compare against an installed HOI4 format reference.'
}

$rasterFiles = @('provinces.bmp', 'heightmap.bmp', 'terrain.bmp', 'rivers.bmp', 'trees.bmp', 'cities.bmp', 'world_normal.bmp')
$rasters = @()
foreach ($raster in $rasterFiles) {
    $path = Assert-File ("map/$raster")
    if (Test-Path -LiteralPath $path) { $rasters += Get-BmpInfo $path }
}
$provinceRaster = $rasters | Where-Object File -eq 'provinces.bmp'
if ($provinceRaster -and ($provinceRaster.Width -ne 5632 -or $provinceRaster.Height -ne 2048)) { Add-ValidationWarning "Unexpected provinces.bmp dimensions: $($provinceRaster.Width)x$($provinceRaster.Height)" }

$rasterColors = $null
$missingRasterColors = @()
$extraRasterColors = @()
if (Test-Path -LiteralPath $provinceMapPath -PathType Leaf) {
    $rasterColors = Get-BmpColors $provinceMapPath
    if ($rasterColors) {
        $definitionColors = New-Object System.Collections.Generic.HashSet[int]
        foreach ($definition in $definitions) { [void]$definitionColors.Add($definition.Color) }
        $missingRasterColors = @($definitions | Where-Object { $_.Id -gt 0 -and -not $rasterColors.Contains($_.Color) } | Select-Object -ExpandProperty Id)
        $extraRasterColors = @($rasterColors | Where-Object { -not $definitionColors.Contains($_) })
        if ($extraRasterColors.Count -gt 0) { Add-ValidationError "provinces.bmp contains RGB colors absent from definition.csv: $($extraRasterColors.Count)" }
        if ($missingRasterColors.Count -gt 0) { Add-ValidationWarning "definition.csv contains province colors absent from provinces.bmp: $($missingRasterColors.Count)" }
    }
}

$outOfBoundsBuildingCoordinates = 0
$malformedBuildingRows = 0
$invalidBuildingProvinceAssociations = 0
$invalidBuildingProvinceIds = New-Object System.Collections.Generic.HashSet[int]
$outOfBoundsUnitStackCoordinates = 0
$malformedUnitStackRows = 0
if ($provinceRaster) {
    foreach ($line in $buildingRows) {
        $parts = $line -split ';'
        if ($parts.Count -lt 7) { $malformedBuildingRows++; continue }
        $x = 0.0; $z = 0.0
        if (-not (Try-ReadInvariantDouble $parts[2].Trim() ([ref]$x)) -or -not (Try-ReadInvariantDouble $parts[4].Trim() ([ref]$z))) { $malformedBuildingRows++; continue }
        if ($x -lt 0 -or $x -ge $provinceRaster.Width -or $z -lt 0 -or $z -ge [math]::Abs($provinceRaster.Height)) { $outOfBoundsBuildingCoordinates++ }
        $provinceAssociation = $parts[6].Trim()
        if ($provinceAssociation -notmatch '^\d+$' -or -not $definitionSet.Contains([int]$provinceAssociation)) {
            $invalidBuildingProvinceAssociations++
            if ($provinceAssociation -match '^\d+$') { [void]$invalidBuildingProvinceIds.Add([int]$provinceAssociation) }
        }
    }
}
if ($malformedBuildingRows -gt 0) { Add-ValidationError "Malformed buildings.txt placement rows: $malformedBuildingRows" }
if ($outOfBoundsBuildingCoordinates -gt 0) { Add-ValidationError "buildings.txt coordinates outside provinces.bmp bounds: $outOfBoundsBuildingCoordinates" }
if ($invalidBuildingProvinceAssociations -gt 0) { Add-ValidationError "buildings.txt rows reference invalid province associations: $invalidBuildingProvinceAssociations (IDs: $($invalidBuildingProvinceIds -join ', '))" }

$unitstacksPath = Assert-File 'map/unitstacks.txt'
$unitstackRows = @(Get-Content -LiteralPath $unitstacksPath | Where-Object { $_ -match ';' })
if ($provinceRaster) {
    foreach ($line in $unitstackRows) {
        $parts = $line -split ';'
        if ($parts.Count -lt 5) { $malformedUnitStackRows++; continue }
        $x = 0.0; $z = 0.0
        if (-not (Try-ReadInvariantDouble $parts[2].Trim() ([ref]$x)) -or -not (Try-ReadInvariantDouble $parts[4].Trim() ([ref]$z))) { $malformedUnitStackRows++; continue }
        if ($x -lt 0 -or $x -ge $provinceRaster.Width -or $z -lt 0 -or $z -ge [math]::Abs($provinceRaster.Height)) { $outOfBoundsUnitStackCoordinates++ }
    }
}
if ($malformedUnitStackRows -gt 0) { Add-ValidationError "Malformed unitstacks.txt placement rows: $malformedUnitStackRows" }
if ($outOfBoundsUnitStackCoordinates -gt 0) { Add-ValidationError "unitstacks.txt coordinates outside provinces.bmp bounds: $outOfBoundsUnitStackCoordinates" }

$railwayPath = Assert-File 'map/railways.txt'
$railwayRows = @(Get-Content -LiteralPath $railwayPath | Where-Object { $_ -match '\S' })
$badRailwayRows = 0
$railwayProvinceRefs = 0
foreach ($line in $railwayRows) {
    $parts = @($line -split '\s+' | Where-Object { $_ -ne '' })
    if ($parts.Count -lt 2 -or $parts[0] -notmatch '^\d+$' -or $parts[1] -notmatch '^\d+$') { $badRailwayRows++; continue }
    $expected = [int]$parts[1]
    $provinceParts = @($parts | Select-Object -Skip 2)
    if ($provinceParts.Count -ne $expected) { $badRailwayRows++; continue }
    foreach ($provinceId in $provinceParts) {
        $railwayProvinceRefs++
        if ($provinceId -notmatch '^\d+$' -or -not $definitionSet.Contains([int]$provinceId)) { $badRailwayRows++ }
    }
}
if ($badRailwayRows -gt 0) { Add-ValidationError "Malformed railways.txt rows or invalid province references: $badRailwayRows" }

$supplyPath = Assert-File 'map/supply_nodes.txt'
$supplyRows = @(Get-Content -LiteralPath $supplyPath | Where-Object { $_ -match '\S' })
$badSupplyRows = 0
foreach ($line in $supplyRows) {
    $parts = @($line -split '\s+' | Where-Object { $_ -ne '' })
    if ($parts.Count -lt 2 -or $parts[0] -notmatch '^\d+$' -or $parts[1] -notmatch '^\d+$' -or -not $definitionSet.Contains([int]$parts[1])) { $badSupplyRows++ }
}
if ($badSupplyRows -gt 0) { Add-ValidationError "Malformed supply_nodes.txt rows or invalid province references: $badSupplyRows" }

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
    RailwayRows = $railwayRows.Count
    RailwayProvinceReferences = $railwayProvinceRefs
    SupplyNodeRows = $supplyRows.Count
    UnitStackRows = $unitstackRows.Count
    EmptyPositionsFile = $positionsEmpty
    ReferencePositionsEmpty = $referencePositionsEmpty
    ProvinceRasterColors = if ($rasterColors) { $rasterColors.Count } else { 0 }
    MissingRasterColors = $missingRasterColors.Count
    ExtraRasterColors = $extraRasterColors.Count
    OutOfBoundsBuildingCoordinates = $outOfBoundsBuildingCoordinates
    InvalidBuildingProvinceAssociations = $invalidBuildingProvinceAssociations
    OutOfBoundsUnitStackCoordinates = $outOfBoundsUnitStackCoordinates
    Errors = $errors.Count
    Warnings = $warnings.Count
    Notes = $notes.Count
}

if ($Json) {
    [pscustomobject]@{ Summary = $summary; Errors = @($errors); Warnings = @($warnings); Notes = @($notes); Rasters = $rasters } | ConvertTo-Json -Depth 5
} else {
    $summary.GetEnumerator() | ForEach-Object { '{0}={1}' -f $_.Key, $_.Value }
    if ($errors.Count -gt 0) { Write-Output 'ERRORS:'; $errors | ForEach-Object { "- $_" } }
    if ($warnings.Count -gt 0) { Write-Output 'WARNINGS:'; $warnings | ForEach-Object { "- $_" } }
    if ($notes.Count -gt 0) { Write-Output 'NOTES:'; $notes | ForEach-Object { "- $_" } }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
