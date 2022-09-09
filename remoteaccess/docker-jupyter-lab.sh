#!/bin/bash

if [ -z "$1" ] ; then
  echo "$0: python|dotnet"
  exit 1
fi

ROOT_DIR="$(dirname "$(readlink -f "$0")")"
ROOT_DIR="$(dirname "$(readlink -f "$ROOT_DIR")")"

source $ROOT_DIR/remoteaccess/env.sh 

if [ "$1" = "python" ] ; then
  IMAGE="jupyter/datascience-notebook:latest"
  IMAGE="jupyter/scipy-notebook:latest"
  PORT=5678

  docker run -it --rm -p $PORT:8888 \
           -e JUPYTER_TOKEN=jupyter \
           -e CLIENT_ID="$CLIENT_ID" \
           -e CLIENT_SECRET="$CLIENT_SECRET" \
           -e AUDIENCE="$AUDIENCE" \
           -e TENANT="$TENANT" \
           -e GRPC_APIS="$GRPC_APIS" \
           -v "$ROOT_DIR/python":"/home/jovyan/notebook-examples/python" \
           --name "jupyter-python" \
           -d $IMAGE
  success=$?
fi

if [ "$1" = "dotnet" ] ; then
  IMAGE="jupyter/dotnet-interactive-notebook:latest"
  PORT=6789

  docker inspect $IMAGE > /dev/null
  inspect=$?
  if [ "$inspect" != "0" ] ; then
    echo "Will now build $IMAGE"
    docker build $ROOT_DIR/remoteaccess --pull -t $IMAGE -f $ROOT_DIR/remoteaccess/.docker/Dockerfile.jupyterlab-dotnet-interactive
    built=$?
    if [ "$built" != "0" ] ; then
      echo "Failed to build $IMAGE"
      exit 1
    fi
  fi

  docker run -it --rm -p $PORT:8888 \
           -e JUPYTER_TOKEN=jupyter \
           -e CLIENT_ID="$CLIENT_ID" \
           -e CLIENT_SECRET="$CLIENT_SECRET" \
           -e AUDIENCE="$AUDIENCE" \
           -e TENANT="$TENANT" \
           -e GRPC_APIS="$GRPC_APIS" \
           -v "$ROOT_DIR/csharp":"/home/jovyan/notebook-examples/csharp" \
           -v "$ROOT_DIR/fsharp":"/home/jovyan/notebook-examples/fsharp" \
           --name "jupyter-dotnet" \
           -d $IMAGE
  success=$?
fi

if [ "$success" == "0" ]; then
  echo
  echo "Point your browser to http://localhost:$PORT/?token=jupyter"
else
  echo
  echo "There was en error"
fi
