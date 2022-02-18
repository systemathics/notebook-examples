# Fill the variables below
$env:CLIENT_ID="<please-fill-in-here>"
$env:CLIENT_SECRET="<please-fill-in-here>"
#$env:TENANT="<please-fill-in-here-if-non-default>"
#$env:AUDIENCE="<please-fill-in-here-if-non-default>"
#$env:GRPC_APIS="<please-fill-in-here-if-non-default>"

[regex]$r = "(CLIENT_ID|CLIENT_SECRET|AUDIENCE|TENANT|GRPC_APIS)"
Get-ChildItem env: | ?{ $r.IsMatch($_.Name) }
