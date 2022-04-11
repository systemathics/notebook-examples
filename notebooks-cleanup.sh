#!/bin/bash

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

pip install nbstripout
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 nbstripout \{};
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i '/^ *"id": "[a-z0-9\-]*",$/d'
#find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis, 0.9.\*-pre\*/nuget: Systemathics.Apis/'
#find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/pip install systemathics.apis --pre/pip install systemathics.apis/'
