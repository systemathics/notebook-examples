#!/bin/bash

ROOT_DIR="$(dirname "$(readlink -f "$0")")"
ROOT_DIR="$(dirname "$(readlink -f "$ROOT_DIR")")"

source $ROOT_DIR/remoteaccess/env.sh 

code "$ROOT_DIR"
