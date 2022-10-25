$env:AUTH0_TOKEN="__AUTH0_TOKEN__"
$env:AUDIENCE="https://ganymede-dev"
$env:TENANT="ganymede-dev.eu.auth0.com"
$env:GRPC_APIS="grpc.dev.systemathics.software"

[regex]$r = "(AUTH0_TOKEN|AUDIENCE|TENANT|GRPC_APIS)"
Get-ChildItem env: | ?{ $r.IsMatch($_.Name) }
