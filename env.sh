
# Fill the variables below using you own token (create tokens in Dashboard -> Tokens)

export CLIENT_ID="YOUR_CLIENT_ID_FROM_DASHBOARD" 
export CLIENT_SECRET="YOUR_CLIENT_SECRET_FROM_DASHBOARD" 
export AUDIENCE="https://prod.ganymede-prod" 
export TENANT="ganymede-prod.eu.auth0.com"
export GRPC_APIS="grpc.systemathics.cloud" 

env | egrep '(CLIENT_ID|CLIENT_SECRET|AUDIENCE|TENANT|GRPC_APIS|AUTH0_TOKEN|SSL_CERT_FILE)'
