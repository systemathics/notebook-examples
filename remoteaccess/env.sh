export CLIENT_ID="<please-fill-in-here>"
export CLIENT_SECRET="<please-fill-in-here>"
export AUDIENCE="https://ganymede-dev"
export TENANT="ganymede-dev.eu.auth0.com"
export GRPC_APIS="grpc.dev.systemathics.software"

env | egrep '(CLIENT_ID|CLIENT_SECRET|AUDIENCE|TENANT|GRPC_APIS)'
