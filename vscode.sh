#!/bin/bash

source env.sh

THIS_SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
code "$THIS_SCRIPT_DIR"
