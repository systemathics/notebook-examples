# Fill the variables below

# remote (prod)
#export CLIENT_ID="Of6cWBNuruUut9cv67yaoFgEGGmgQnEd"
#export CLIENT_SECRET="xNolGV_-w-blBHRFX_h5KiLFtKBSHDy2Qv7MIGlaysakupMK2_wQZBF_8jEredqi"

# remote (dev)
#export CLIENT_ID="Of6cWBNuruUut9cv67yaoFgEGGmgQnEd"
#export CLIENT_SECRET="xNolGV_-w-blBHRFX_h5KiLFtKBSHDy2Qv7MIGlaysakupMK2_wQZBF_8jEredqi"
#export TENANT="ganymede-dev.eu.auth0.com"
#export AUDIENCE="https://dev.ganymede-dev"
#export GRPC_APIS="https://grpc.dev.systemathics.eu"

# local
export GRPC_APIS="http://172.29.32.1:5000" # windows

env | egrep '(CLIENT_ID|CLIENT_SECRET|AUDIENCE|TENANT|GRPC_APIS)'
