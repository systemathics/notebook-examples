export AUTH0_TOKEN="__AUTH0_TOKEN__"
export AUDIENCE="https://ganymede-prod"
export TENANT="ganymede-prod.eu.auth0.com"
export GRPC_APIS="grpc.ganymede.cloud"

env | egrep '(AUTH0_TOKEN|AUDIENCE|TENANT|GRPC_APIS)'
