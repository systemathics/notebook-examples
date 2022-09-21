#!/bin/bash

branch=$1
if [ -z "$branch" ] ; then
  branch=$(git rev-parse --abbrev-ref HEAD)
fi

if [ "$branch" = "dev" ] ; then
  echo "Using pre-release Systemathics.Apis (and dev.ganymede.software)"	
elif [ "$branch" = "prod" ] ; then
  echo "Using production Systemathics.Apis (and ganymede.cloud)"	
else
  echo "Don't know how to handle branch $branch"
  exit 1
fi

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

DOS2UNIX=$(which dos2unix)
if [ ! -z "$DOS2UNIX" ] ; then
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 dos2unix \{} >& /dev/null;
fi
 
export PATH=$HOME/.local/bin:$PATH
NBSTRIPOUT=$(which nbstripout)
if [ -z "$NBSTRIPOUT" ] ; then
  pip install nbstripout
fi
NBSTRIPOUT=$(which nbstripout)
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 $NBSTRIPOUT --drop-empty-cells --strip-init-cells \{}; 

# cleanup any pre-release mention (python)
find $ROOT_DIR/python -name "*.ipynb" -print0 | xargs -0 sed -i 's/"\(pip install systemathics.apis\).*"/"\1"/'
find $ROOT_DIR/csharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/#r\s*.*\(\\"nuget:\s*Systemathics.Apis\).*\(\\"\)/#r \1\2/'
find $ROOT_DIR/fsharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/#r\s*.*\(\\"nuget:\s*Systemathics.Apis\).*\(\\"\)/#r \1\2/'

# rewrite URLs
find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's|https://dev\.ganymede\.software|https://ganymede.cloud|g'
find $ROOT_DIR -name "*.md" -print0 | xargs -0 sed -i 's|https://dev\.ganymede\.software|https://ganymede.cloud|g'
sed -i 's|ganymede-dev|ganymede-prod|g' remoteaccess/env.sh
sed -i 's|ganymede-dev|ganymede-prod|g' remoteaccess/env.ps1
sed -i 's|dev\.systemathics\.software|ganymede.cloud|g' remoteaccess/env.sh
sed -i 's|dev\.systemathics\.software|ganymede.cloud|g' remoteaccess/env.ps1

if [ "$branch" = "dev" ] ; then
  # apply pre-release mention
  find $ROOT_DIR/csharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis, 0.\*-pre\*/'
  find $ROOT_DIR/fsharp -name "*.ipynb" -print0 | xargs -0 sed -i 's/nuget: Systemathics.Apis/nuget: Systemathics.Apis, 0.\*-pre\*/'
  find $ROOT_DIR/python -name "*.ipynb" -print0 | xargs -0 sed -i 's/pip install systemathics.apis/pip install systemathics.apis --pre/'

  # rewrite URLs
  find $ROOT_DIR -name "*.ipynb" -print0 | xargs -0 sed -i 's|https://ganymede\.cloud|https://dev.ganymede.software|g'
  find $ROOT_DIR -name "*.md" -print0 | xargs -0 sed -i 's|https://ganymede\.cloud|https://dev.ganymede.software|g'
  sed -i 's|ganymede-prod|ganymede-dev|g' remoteaccess/env.sh
  sed -i 's|ganymede-prod|ganymede-dev|g' remoteaccess/env.ps1
  sed -i 's|ganymede\.cloud|dev.systemathics.software|g' remoteaccess/env.sh
  sed -i 's|ganymede\.cloud|dev.systemathics.software|g' remoteaccess/env.ps1
fi

du -sh csharp/
du -sh fsharp/
du -sh csharp/