@echo off

set AUTH0_TOKEN="__AUTH0_TOKEN__"
set AUDIENCE="https://ganymede-prod"
set TENANT="ganymede-prod.eu.auth0.com"
set GRPC_APIS="grpc.ganymede.cloud"

REM Launches Jupyter lab from the python notebooks folder
jupyter-lab.exe ..\python
