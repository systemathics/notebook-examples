#!/bin/bash

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "prod" ] ; then
  echo "Rewriting notebooks to use stable Systemathics.Apis (current git branch: prod)"
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis/'
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/pip install systemathics.apis/pip install systemathics.apis/'
elif [ "$branch" = "master" ] ; then
  echo "Rewriting notebooks to use pre-release Systemathics.Apis (current git branch: master)"	
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis, 0.11.\*-pre\*/'
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's/pip install systemathics.apis/pip install systemathics.apis --pre/'
else
  echo "Don't know how to handle branch $branch"
  exit 1
fi

export PATH=$HOME/.local/bin:$PATH

NBSTRIPOUT=$(which nbstripout)
if [ -z "$NBSTRIPOUT" ] ; then
  pip install nbstripout
fi

NBSTRIPOUT=$(which nbstripout)
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 $NBSTRIPOUT \{};

DOS2UNIX=$(which dos2unix)
if [ ! -z "$DOS2UNIX" ] ; then
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 dos2unix \{};
fi

