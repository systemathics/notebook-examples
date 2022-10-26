$env:AUTH0_TOKEN="__AUTH0_TOKEN__"
$env:AUDIENCE="https://ganymede-prod"
$env:TENANT="ganymede-prod.eu.auth0.com"
$env:GRPC_APIS="grpc.ganymede.cloud"

[regex]$r = "(AUTH0_TOKEN|AUDIENCE|TENANT|GRPC_APIS)"
Get-ChildItem env: | ?{ $r.IsMatch($_.Name) }
