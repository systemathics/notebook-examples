
$root = (Get-Item $PSScriptRoot).Parent.FullName
$env = Join-Path $root "remoteaccess"
$env = Join-Path $env "env.ps1"

. $env
& jupyter-lab.exe $root
