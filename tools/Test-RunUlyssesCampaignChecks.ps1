[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('ulysses-wrapper-' + [guid]::NewGuid().ToString('N'))
$oldPath = $env:PATH
New-Item -ItemType Directory -Path $fixture | Out-Null

try {
    # Force the first child command to fail. The aggregate wrapper must return
    # nonzero instead of continuing to later checks and reporting success.
    Set-Content -LiteralPath (Join-Path $fixture 'python.cmd') -Value "@echo off`r`nexit /b 17" -Encoding ascii
    $env:PATH = "$fixture;$oldPath"
    & pwsh -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Run-UlyssesCampaignChecks.ps1')
    if ($LASTEXITCODE -eq 0) {
        throw 'Expected the aggregate wrapper to fail when its first child fails.'
    }
    Write-Output 'Wrapper negative regression passed: child failure propagates.'
}
finally {
    $env:PATH = $oldPath
    Remove-Item -LiteralPath $fixture -Recurse -Force -ErrorAction SilentlyContinue
}
