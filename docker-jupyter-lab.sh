#!/bin/bash

source env.sh 

THIS_SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
docker run -it --rm -p 8888:8888 \
           -e JUPYTER_ENABLE_LAB=yes \
           -e JUPYTER_TOKEN=jupyter \
           -e CLIENT_ID="$CLIENT_ID" \
           -e CLIENT_SECRET="$CLIENT_SECRET" \
           -e AUDIENCE="$AUDIENCE" \
           -e TENANT="$TENANT" \
           -e GRPC_APIS="$GRPC_APIS" \
           -v "$THIS_SCRIPT_DIR/python":"/home/jovyan/notebook-examples/python" \
           --name jupyter \
           -d jupyter/datascience-notebook:latest
success=$?

if [ "$success" == "0" ]; then
    echo
    echo "Point your browser to http://localhost:8888/?token=jupyter"
else
    echo
    echo "There was en error"
fi
