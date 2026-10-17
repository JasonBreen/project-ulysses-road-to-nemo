[CmdletBinding()]
param([string]$PythonCommand = 'python')

$ErrorActionPreference = 'Stop'
& $PythonCommand -m unittest discover -s $PSScriptRoot -p test_economy.py -v
if ($LASTEXITCODE -ne 0) { throw "Economy checks failed with exit code $LASTEXITCODE" }
