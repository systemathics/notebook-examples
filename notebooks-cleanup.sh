#!/bin/bash

branch=$1
if [ -z "$branch" ] ; then
  branch=$(git rev-parse --abbrev-ref HEAD)
fi

if [ "$branch" = "dev" ] ; then
  echo "Using pre-release Systemathics.Apis"	
elif [ "$branch" = "prod" ] ; then
  echo "Using production Systemathics.Apis"	
else
  echo "Don't know how to handle branch $branch"
  exit 1
fi

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

# cleanup any pre-release mention (python)
find $ROOT_DIR/python -name "*.ipynb" -print0 | xargs -0 sed -i 's/"\(pip install systemathics.apis\).*"/"\1"/'

# cleanup any pre-release mention (dotnet)
find $ROOT_DIR/csharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/#r\s*.*\(\\"nuget:\s*Systemathics.Apis\).*\(\\"\)/#r \1\2/'
find $ROOT_DIR/fsharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/#r\s*.*\(\\"nuget:\s*Systemathics.Apis\).*\(\\"\)/#r \1\2/'

if [ "$branch" = "dev" ] ; then
  # apply pre-release mention
  find $ROOT_DIR/csharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis, 0.\*-pre\*/'
  find $ROOT_DIR/fsharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis, 0.\*-pre\*/'
  # apply pre-release mention
  find $ROOT_DIR/python -name "*.ipynb" -print0 | xargs -0 sed -i 's/pip install systemathics.apis/pip install systemathics.apis --pre/'
fi

export PATH=$HOME/.local/bin:$PATH

NBSTRIPOUT=$(which nbstripout)
if [ -z "$NBSTRIPOUT" ] ; then
  pip install nbstripout
fi

NBSTRIPOUT=$(which nbstripout)
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 $NBSTRIPOUT --drop-empty-cells --strip-init-cells \{} >& /dev/null; 

DOS2UNIX=$(which dos2unix)
if [ ! -z "$DOS2UNIX" ] ; then
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 dos2unix \{} >& /dev/null;
fi
 