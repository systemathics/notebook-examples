@echo off

set AUTH0_TOKEN="__AUTH0_TOKEN__"
set AUDIENCE="https://ganymede-dev"
set TENANT="ganymede-dev.eu.auth0.com"
set GRPC_APIS="grpc.dev.systemathics.software"

REM Launches Jupyter lab from the python notebooks folder
jupyter-lab.exe ..\python
