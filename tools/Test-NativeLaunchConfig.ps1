[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProfileRoot,
    [string]$DescriptorPath,
    [string]$PayloadRoot,
    [string]$DlcLoadPath,
    [string]$LauncherSettingsPath,
    [string]$LauncherBackupPath,
    [string]$ExpectedSourceRoot,
    [switch]$PlanOnly
)

$ErrorActionPreference = 'Stop'

function Resolve-ExistingPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Required path does not exist: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).Path
}

function Normalize-Path {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [IO.Path]::GetFullPath($Path).TrimEnd('\')
}

function Assert-Under {
    param(
        [Parameter(Mandatory = $true)][string]$Child,
        [Parameter(Mandatory = $true)][string]$Parent,
        [Parameter(Mandatory = $true)][string]$Label
    )
    $childPath = Normalize-Path $Child
    $parentPath = Normalize-Path $Parent
    if (-not $childPath.Equals($parentPath, [StringComparison]::OrdinalIgnoreCase) -and
        -not $childPath.StartsWith($parentPath + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "$Label escapes its intended profile: $childPath"
    }
}

function Assert-NoForbiddenText {
    param([Parameter(Mandatory = $true)][string]$Text, [Parameter(Mandatory = $true)][string]$Label)
    if ($Text -match '(?i)millennium[-_ ]?dawn|md[_-]?oem|millennium-dawn-oem|vanilla') {
        throw "$Label contains a forbidden Millennium Dawn/OEM/vanilla marker."
    }
}

$profile = Normalize-Path $ProfileRoot
$normalUserData = Normalize-Path ([IO.Path]::Combine([Environment]::GetFolderPath('MyDocuments'), 'Paradox Interactive', 'Hearts of Iron IV'))
if ($profile.Equals($normalUserData, [StringComparison]::OrdinalIgnoreCase) -or
    $profile.StartsWith($normalUserData + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to use the normal HOI4 user-data tree as an isolated profile: $profile"
}

if ($ExpectedSourceRoot) {
    $source = Resolve-ExistingPath $ExpectedSourceRoot
    Assert-NoForbiddenText -Text $source -Label 'Expected source path'
    if (-not (Test-Path -LiteralPath (Join-Path $source 'common')) -or
        -not (Test-Path -LiteralPath (Join-Path $source 'history')) -or
        -not (Test-Path -LiteralPath (Join-Path $source 'map'))) {
        throw "Expected source root is not a complete Ulysses mod root: $source"
    }
}

if ($LauncherSettingsPath -and $LauncherBackupPath) {
    $settings = Resolve-ExistingPath $LauncherSettingsPath
    $backup = Resolve-ExistingPath $LauncherBackupPath
    $settingsHash = (Get-FileHash -LiteralPath $settings -Algorithm SHA256).Hash
    $backupHash = (Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash
    if ($settingsHash -ne $backupHash) {
        throw "Launcher settings differ from the preserved baseline: $settings"
    }
    Write-Output "LauncherSettingsPreserved=True"
}

if ($PlanOnly) {
    $plannedDescriptor = Join-Path $profile 'mod\ProjectUlysses_native_reviewfix_20261018.mod'
    $plannedPayload = Join-Path $profile 'mod\ProjectUlysses_native_reviewfix_20261018'
    $plannedDlc = Join-Path $profile 'dlc_load.json'
    Write-Output "PlanOnly=True"
    Write-Output "UserDataOverride=$profile"
    Write-Output "Descriptor=$plannedDescriptor"
    Write-Output "Payload=$plannedPayload"
    Write-Output "DlcLoad=$plannedDlc"
    Write-Output "LaunchArguments=-userdir=$profile -mod=$plannedDescriptor"
    Write-Output 'RuntimeIsolationProven=False'
    exit 0
}

$descriptor = Resolve-ExistingPath ($DescriptorPath ?? (Join-Path $profile 'mod\ProjectUlysses_native_reviewfix_20261018.mod'))
$payload = Resolve-ExistingPath ($PayloadRoot ?? (Join-Path $profile 'mod\ProjectUlysses_native_reviewfix_20261018'))
$dlcLoad = Resolve-ExistingPath ($DlcLoadPath ?? (Join-Path $profile 'dlc_load.json'))
Assert-Under -Child $descriptor -Parent (Join-Path $profile 'mod') -Label 'Descriptor'
Assert-Under -Child $payload -Parent (Join-Path $profile 'mod') -Label 'Payload'

$descriptorText = Get-Content -LiteralPath $descriptor -Raw
$pathMatch = [regex]::Match($descriptorText, '(?m)^path\s*=\s*"([^"]+)"\s*$')
if (-not $pathMatch.Success) { throw "Descriptor has no exact path= entry: $descriptor" }
$declaredPayload = Normalize-Path $pathMatch.Groups[1].Value.Replace('/', '\')
if ($declaredPayload -ne (Normalize-Path $payload)) {
    throw "Descriptor path does not resolve to the profile-local payload: $declaredPayload"
}
Assert-NoForbiddenText -Text ($descriptorText + $descriptor) -Label 'Ulysses descriptor'

$load = Get-Content -LiteralPath $dlcLoad -Raw | ConvertFrom-Json
$enabled = @($load.enabled_mods)
if ($enabled.Count -ne 1) { throw "Expected exactly one enabled mod, found $($enabled.Count)." }
$expectedRelative = ('mod/' + (Split-Path -Leaf $descriptor))
if ($enabled[0] -ne $expectedRelative) {
    throw "dlc_load.json selects '$($enabled[0])' instead of '$expectedRelative'."
}
Assert-NoForbiddenText -Text (Get-Content -LiteralPath $dlcLoad -Raw) -Label 'dlc_load.json'

$topLevel = @(Get-ChildItem -LiteralPath (Join-Path $profile 'mod') -Force)
$unexpected = @($topLevel | Where-Object { $_.FullName -ne $descriptor -and $_.FullName -ne $payload })
if ($unexpected.Count -gt 0) { throw "Profile mod directory contains unexpected entries: $($unexpected.Name -join ', ')" }
foreach ($required in @('descriptor.mod', 'common', 'history', 'map', 'localisation')) {
    if (-not (Test-Path -LiteralPath (Join-Path $payload $required))) {
        throw "Profile payload is incomplete; missing $required."
    }
}

Write-Output "Profile=$profile"
Write-Output "Descriptor=$descriptor"
Write-Output "Payload=$payload"
Write-Output "EnabledMod=$($enabled[0])"
Write-Output 'StaticLaunchConfig=PASS'
Write-Output 'RuntimeIsolationProven=False'
