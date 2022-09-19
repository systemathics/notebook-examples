# Fill the variables below
$env:CLIENT_ID="<please-fill-in-here>"
$env:CLIENT_SECRET="<please-fill-in-here>"
$env:AUDIENCE="https://ganymede-dev"
$env:TENANT="ganymede-dev.eu.auth0.com"
$env:GRPC_APIS="grpc.dev.systemathics.software"

[regex]$r = "(CLIENT_ID|CLIENT_SECRET|AUDIENCE|TENANT|GRPC_APIS)"
Get-ChildItem env: | ?{ $r.IsMatch($_.Name) }
