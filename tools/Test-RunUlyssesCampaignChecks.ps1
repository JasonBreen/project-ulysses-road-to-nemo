[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('ulysses-wrapper-' + [guid]::NewGuid().ToString('N'))
$oldPath = $env:PATH
New-Item -ItemType Directory -Path $fixture | Out-Null
$currentHost = if ($PSVersionTable.PSEdition -eq 'Core') { Join-Path $PSHOME 'pwsh.exe' } else { Join-Path $PSHOME 'powershell.exe' }
$hostCandidates = @($currentHost)
if ($PSVersionTable.PSEdition -eq 'Core') {
    $alternateHost = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
} else {
    $alternateHost = (Get-Command pwsh.exe -ErrorAction SilentlyContinue).Path
}
if ($alternateHost -and (Test-Path -LiteralPath $alternateHost -PathType Leaf) -and ($hostCandidates -notcontains $alternateHost)) {
    $hostCandidates += $alternateHost
}

try {
    # Force the first child command to fail. The aggregate wrapper must return
    # nonzero instead of continuing to later checks and reporting success.
    Set-Content -LiteralPath (Join-Path $fixture 'python.cmd') -Value "@echo off`r`nexit /b 17" -Encoding ascii
    $env:PATH = "$fixture;$oldPath"
    foreach ($scriptHost in $hostCandidates) {
        Write-Output "Testing aggregate wrapper host: $scriptHost"
        & $scriptHost -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Run-UlyssesCampaignChecks.ps1')
        if ($LASTEXITCODE -eq 0) {
            throw "Expected the aggregate wrapper to fail when its first child fails under $scriptHost."
        }
    }
    Write-Output 'Wrapper negative regression passed: child failure propagates.'
}
finally {
    $env:PATH = $oldPath
    Remove-Item -LiteralPath $fixture -Recurse -Force -ErrorAction SilentlyContinue
}
