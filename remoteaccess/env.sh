export AUTH0_TOKEN="__AUTH0_TOKEN__"
export AUDIENCE="https://ganymede-dev"
export TENANT="ganymede-dev.eu.auth0.com"
export GRPC_APIS="grpc.dev.systemathics.software"

env | egrep '(AUTH0_TOKEN|AUDIENCE|TENANT|GRPC_APIS)'
