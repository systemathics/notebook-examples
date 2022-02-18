#!/bin/bash

ROOT_DIR="$(dirname "$(readlink -f "$0")")"
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output --inplace $ROOT_DIR/\*/\*/\*.ipynb
