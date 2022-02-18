#!/bin/bash

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

pip install nbstripout
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 nbstripout \{};
