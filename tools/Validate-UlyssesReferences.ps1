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
$notes = New-Object System.Collections.Generic.List[string]

function Add-ReferenceError([string]$Message) { [void]$script:errors.Add($Message) }
function Add-ReferenceWarning([string]$Message) { [void]$script:warnings.Add($Message) }
function Add-ReferenceNote([string]$Message) { [void]$script:notes.Add($Message) }
function Strip-Comment([string]$Line) {
    if ($null -eq $Line) { return '' }
    return ([regex]::Replace($Line, '#.*$', '')).Trim()
}
function Add-SetValue([System.Collections.Generic.HashSet[string]]$Set, [string]$Value) {
    if ($Value) { [void]$Set.Add($Value) }
}

$codeFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File -Include *.txt | Where-Object { $_.FullName -notmatch '\\localisation\\' })
$eventFiles = @(Get-ChildItem -LiteralPath (Join-Path $root 'events') -File -Filter *.txt)
$focusFiles = @(Get-ChildItem -LiteralPath (Join-Path $root 'common\national_focus') -File -Filter *.txt)
$localisationFiles = @(Get-ChildItem -LiteralPath (Join-Path $root 'localisation') -Recurse -File -Filter *.yml)

$focusIds = New-Object System.Collections.Generic.HashSet[string]
foreach ($file in $focusFiles) {
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $clean = Strip-Comment $line
        if ($clean -match '^\s*id\s*=\s*([A-Za-z0-9_]+)\s*$') { Add-SetValue $focusIds $Matches[1] }
    }
}

$focusRefs = New-Object System.Collections.Generic.List[object]
foreach ($file in $focusFiles) {
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $lineNumber++
        $clean = Strip-Comment $line
        foreach ($match in [regex]::Matches($clean, '(?:^|\s)(?:focus|relative_position_id|shared_focus)\s*=\s*([A-Za-z0-9_]+)')) {
            $value = $match.Groups[1].Value
            if ($value -ne 'focus' -and $value -ne 'none') {
                $focusRefs.Add([pscustomobject]@{ Id = $value; File = $file.FullName; Line = $lineNumber })
            }
        }
    }
}
$missingFocusRefs = @($focusRefs | Where-Object { -not $focusIds.Contains($_.Id) } | Sort-Object Id,File,Line -Unique)
foreach ($reference in $missingFocusRefs) { Add-ReferenceError "Focus reference '$($reference.Id)' is not defined ($($reference.File):$($reference.Line))" }

$eventIds = New-Object System.Collections.Generic.HashSet[string]
$eventLocations = @{}
$eventDefinitionRows = New-Object System.Collections.Generic.List[object]
foreach ($file in $eventFiles) {
    $lineNumber = 0
    $braceDepth = 0
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $lineNumber++
        $clean = Strip-Comment $line
        if ($braceDepth -eq 1 -and $clean -match '^\s*id\s*=\s*([A-Za-z0-9_]+\.\d+)') {
            $id = $Matches[1]
            Add-SetValue $eventIds $id
            [void]$eventDefinitionRows.Add([pscustomobject]@{ Id = $id; File = $file.FullName; Line = $lineNumber })
            if (-not $eventLocations.ContainsKey($id)) { $eventLocations[$id] = "{0}:{1}" -f $file.FullName,$lineNumber }
        }
        $braceDepth += ([regex]::Matches($clean, '\{')).Count
        $braceDepth -= ([regex]::Matches($clean, '\}')).Count
        if ($braceDepth -lt 0) { $braceDepth = 0 }
    }
}
$duplicateEventDefinitions = @($eventDefinitionRows | Group-Object Id | Where-Object Count -gt 1)
foreach ($duplicate in $duplicateEventDefinitions) {
    $locations = ($duplicate.Group | ForEach-Object { "{0}:{1}" -f $_.File,$_.Line }) -join ', '
    Add-ReferenceError "Duplicate event definition '$($duplicate.Name)' at $locations"
}
$ownedEventNamespaces = New-Object System.Collections.Generic.HashSet[string]
foreach ($id in $eventIds) { Add-SetValue $ownedEventNamespaces ($id -split '\.')[0] }

$eventRefs = New-Object System.Collections.Generic.List[object]
$malformedEventRefs = New-Object System.Collections.Generic.List[object]
foreach ($file in $codeFiles) {
    $lines = @(Get-Content -LiteralPath $file.FullName)
    $lineNumber = 0
    foreach ($sourceLine in $lines) {
        $lineNumber++
        $cleanLine = Strip-Comment $sourceLine
        if ($cleanLine -match '(?:country_event|news_event|trigger_event|fire_event)\s*=\s*([^\s#]+)' -and $Matches[1] -ne '{' -and $Matches[1] -notmatch '^[A-Za-z0-9_]+\.\d+$') {
            [void]$malformedEventRefs.Add([pscustomobject]@{ Target = $Matches[1]; File = $file.FullName; Line = $lineNumber })
        }
    }
    $text = $lines -join "`n"
    if ($null -eq $text) { $text = '' }
    $cleanText = [regex]::Replace($text, '(?m)#.*$', '')
    foreach ($match in [regex]::Matches($cleanText, '(?:country_event|news_event|trigger_event|fire_event)\s*=\s*(?:\{\s*)?(?:id\s*=\s*)?([A-Za-z0-9_]+\.\d+)')) {
        $id = $match.Groups[1].Value
        $prefix = $cleanText.Substring(0, $match.Index)
        $line = ([regex]::Matches($prefix, "`n")).Count + 1
        $eventRefs.Add([pscustomobject]@{ Id = $id; File = $file.FullName; Line = $line })
    }
}
$malformedEventRefs = @($malformedEventRefs | Sort-Object Target,File,Line -Unique)
foreach ($reference in $malformedEventRefs) { Add-ReferenceError "Malformed event target '$($reference.Target)' ($($reference.File):$($reference.Line))" }
$missingEventRefs = @($eventRefs | Where-Object { $ownedEventNamespaces.Contains(($_.Id -split '\.')[0]) -and -not $eventIds.Contains($_.Id) } | Sort-Object Id,File,Line -Unique)
foreach ($reference in $missingEventRefs) { Add-ReferenceError "Owned event reference '$($reference.Id)' is not defined ($($reference.File):$($reference.Line))" }
$externalEventNamespaces = @($eventRefs | Where-Object { -not $ownedEventNamespaces.Contains(($_.Id -split '\.')[0]) } | ForEach-Object { ($_.Id -split '\.')[0] } | Sort-Object -Unique)
if ($externalEventNamespaces.Count -gt 0) { Add-ReferenceNote "External/vanilla event namespaces intentionally not resolved: $($externalEventNamespaces -join ', ')" }

$scriptedDefinitions = New-Object System.Collections.Generic.HashSet[string]
foreach ($directory in @('common\scripted_effects', 'common\scripted_triggers')) {
    $path = Join-Path $root $directory
    foreach ($file in Get-ChildItem -LiteralPath $path -File -Filter *.txt) {
        foreach ($line in Get-Content -LiteralPath $file.FullName) {
            $clean = Strip-Comment $line
            if ($clean -match '^([A-Za-z][A-Za-z0-9_]*)\s*=\s*\{') { Add-SetValue $scriptedDefinitions $Matches[1] }
        }
    }
}
$scriptCallFiles = @($codeFiles | Where-Object { $_.FullName -match '\\events\\|\\common\\national_focus\\|\\common\\decisions\\|\\common\\on_actions\\|\\common\\ideas\\|\\common\\bop\\' })
$scriptedReferences = New-Object System.Collections.Generic.HashSet[string]
foreach ($file in $scriptCallFiles) {
    $scriptText = Get-Content -LiteralPath $file.FullName -Raw
    if ($null -eq $scriptText) { $scriptText = '' }
    $cleanText = [regex]::Replace($scriptText, '(?m)#.*$', '')
    # The previous implementation tested every scripted definition against
    # every call file. On this mod that becomes an O(definitions * files)
    # regex loop and can appear hung for several minutes. Scan each file once
    # for the same line-start assignment shape, then retain only known
    # scripted definitions. This preserves the audit's scope while making the
    # cost linear in the amount of source text.
    foreach ($match in [regex]::Matches($cleanText, '(?m)^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*\{')) {
        $candidate = $match.Groups[1].Value
        if ($scriptedDefinitions.Contains($candidate)) { Add-SetValue $scriptedReferences $candidate }
    }
}

$locKeys = New-Object System.Collections.Generic.HashSet[string]
$emptyLocKeys = New-Object System.Collections.Generic.HashSet[string]
foreach ($file in $localisationFiles) {
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        # HOI4 accepts both versioned `key:0 "text"` and versionless
        # `key: "text"` entries; inherited archive files use the latter.
        if ($line -match '^\s*([A-Za-z0-9_.-]+):\d*\s*"') {
            $key = $Matches[1]
            Add-SetValue $locKeys $key
            if ($line -match ':\d*\s*""\s*$') { Add-SetValue $emptyLocKeys $key }
        }
    }
}

$eventLocRefs = New-Object System.Collections.Generic.List[object]
foreach ($file in $eventFiles) {
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $lineNumber++
        $clean = Strip-Comment $line
        if ($clean -match '^\s*(?:title|desc|name|custom_effect_tooltip)\s*=\s*([A-Za-z0-9_.-]+)') {
            $key = $Matches[1]
            # Event localization IDs are not required to contain a dot.  The
            # original audit silently skipped underscore-only keys such as
            # custom_effect_tooltip IDs, allowing missing UI text to pass.
            $eventLocRefs.Add([pscustomobject]@{ Key = $key; File = $file.FullName; Line = $lineNumber })
        }
    }
}
$missingEventLoc = @($eventLocRefs | Where-Object { -not $locKeys.Contains($_.Key) } | Sort-Object Key,File,Line -Unique)
foreach ($reference in $missingEventLoc) { Add-ReferenceWarning "Localization key '$($reference.Key)' is missing ($($reference.File):$($reference.Line))" }
$emptyEventLoc = @($eventLocRefs | Where-Object { $emptyLocKeys.Contains($_.Key) } | Sort-Object Key,File,Line -Unique)
foreach ($reference in $emptyEventLoc) { Add-ReferenceWarning "Localization key '$($reference.Key)' is present but empty ($($reference.File):$($reference.Line))" }

$missingFocusLoc = @()
foreach ($id in $focusIds) {
    foreach ($key in @($id, "${id}_desc")) {
        if (-not $locKeys.Contains($key)) { $missingFocusLoc += $key }
        elseif ($emptyLocKeys.Contains($key)) { Add-ReferenceWarning "Focus localization key '$key' is present but empty" }
    }
}
foreach ($key in @($missingFocusLoc | Sort-Object -Unique)) { Add-ReferenceWarning "Focus localization key '$key' is missing" }

$historyCountryPath = Join-Path $root 'history\countries'
$commonCountryPath = Join-Path $root 'common\countries'
$historyTags = New-Object System.Collections.Generic.HashSet[string]
$missingCountryDefinitions = New-Object System.Collections.Generic.List[string]
foreach ($file in Get-ChildItem -LiteralPath $historyCountryPath -File -Filter *.txt) {
    if ($file.BaseName -notmatch '^([A-Z0-9]{3})\s+-\s+(.+)$') { Add-ReferenceWarning "Country history filename does not expose a three-letter tag: $($file.Name)"; continue }
    $tag = $Matches[1]; $countryName = $Matches[2]
    Add-SetValue $historyTags $tag
    # Common country filenames are not tag declarations; the history filename is the reliable tag source.
    if (-not $locKeys.Contains($tag)) { [void]$missingCountryDefinitions.Add("$tag -> missing country localization") }
}
foreach ($item in $missingCountryDefinitions) { Add-ReferenceWarning "Country history has no matching country localization key: $item" }

$summary = [ordered]@{
    FocusDefinitions = $focusIds.Count
    FocusReferences = $focusRefs.Count
    MissingFocusReferences = $missingFocusRefs.Count
    EventDefinitions = $eventIds.Count
    DuplicateEventDefinitions = $duplicateEventDefinitions.Count
    EventReferences = $eventRefs.Count
    MissingOwnedEventReferences = $missingEventRefs.Count
    MalformedEventReferences = $malformedEventRefs.Count
    ScriptedDefinitions = $scriptedDefinitions.Count
    ScriptedReferences = $scriptedReferences.Count
    LocalizationKeys = $locKeys.Count
    MissingEventLocalization = $missingEventLoc.Count
    EmptyEventLocalization = $emptyEventLoc.Count
    MissingFocusLocalization = @($missingFocusLoc | Sort-Object -Unique).Count
    CountryHistories = $historyTags.Count
    MissingCountryDefinitions = $missingCountryDefinitions.Count
    Errors = $errors.Count
    Warnings = $warnings.Count
    Notes = $notes.Count
}

if ($Json) {
    [pscustomobject]@{ Summary = $summary; Errors = @($errors); Warnings = @($warnings); Notes = @($notes) } | ConvertTo-Json -Depth 5
} else {
    $summary.GetEnumerator() | ForEach-Object { '{0}={1}' -f $_.Key, $_.Value }
    if ($errors.Count -gt 0) { Write-Output 'ERRORS:'; $errors | ForEach-Object { "- $_" } }
    if ($warnings.Count -gt 0) { Write-Output 'WARNINGS:'; $warnings | ForEach-Object { "- $_" } }
    if ($notes.Count -gt 0) { Write-Output 'NOTES:'; $notes | ForEach-Object { "- $_" } }
}

if ($errors.Count -gt 0) { exit 1 }
exit 0
