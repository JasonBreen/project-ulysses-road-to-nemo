[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('ulysses-no-vanilla-' + [guid]::NewGuid().ToString('N'))
$mod = Join-Path $fixture 'mod'
$reference = Join-Path $fixture 'reference'
$baseline = Join-Path $fixture 'baseline'
$relative = 'common\example.txt'

try {
    foreach ($root in @($mod, $reference, $baseline)) {
        New-Item -ItemType Directory -Path (Join-Path $root 'common') -Force | Out-Null
    }

    $descriptor = "version=`"0.3-dev`"`nname=`"Fixture`"`nsupported_version=`"1.19.*`"`n"
    [IO.File]::WriteAllText((Join-Path $fixture '2985041246.mod'), $descriptor, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $mod 'descriptor.mod'), $descriptor, [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $mod 'ProjectUlysses.mod'), $descriptor, [Text.UTF8Encoding]::new($false))

    # The mod and reference use LF; the preserved baseline uses CRLF. The
    # provenance audit must classify this as inherited, not a new vanilla file.
    [IO.File]::WriteAllText((Join-Path $mod $relative), "alpha`nbeta`n", [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $reference $relative), "alpha`nbeta`n", [Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText((Join-Path $baseline $relative), "alpha`r`nbeta`r`n", [Text.UTF8Encoding]::new($false))

    $output = & pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Validate-NoVanillaAssets.ps1') `
        -ModRoot $mod -ReferenceGameRoot $reference -BaselineRoot $baseline -Json | Out-String
    if ($LASTEXITCODE -ne 0) { throw "Validator exited with code $LASTEXITCODE`n$output" }
    $report = $output | ConvertFrom-Json
    if ([int]$report.Summary.NewVanillaMatches -ne 0) {
        throw "CRLF/LF-equivalent fixture was classified as new vanilla content: $output"
    }
    if ([int]$report.Summary.InheritedVanillaMatches -ne 1) {
        throw "Expected one inherited text match: $output"
    }
    Write-Output 'No-vanilla provenance regression passed: CRLF/LF-only differences are inherited.'
}
finally {
    if (Test-Path -LiteralPath $fixture) {
        Remove-Item -LiteralPath $fixture -Recurse -Force
    }
}
