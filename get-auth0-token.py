#!/usr/bin/python3

import os
import subprocess
import sys
import re

if (not(len(sys.argv) == 3)):
  raise Exception("Usage: get-auth0-token.py client_id client_secret")

os.environ["CLIENT_ID"]     = clientid = sys.argv[1]
os.environ["CLIENT_SECRET"] = clientsecret = sys.argv[2]
os.environ["AUDIENCE"]      ="https://ganymede-dev"
os.environ["TENANT"]        ="ganymede-dev.eu.auth0.com"

# Ensure systemathics.apis is installed
with os.popen("git rev-parse --abbrev-ref HEAD") as pipe:
  branch = pipe.read()
if (branch is None):
  raise Exception("Cannot infer branch")
branch = branch.strip()
if (branch == "dev"):
  subprocess.check_call([sys.executable, "-m", "pip", "install", "systemathics.apis", "--pre"])
elif (branch == "prod"):
  subprocess.check_call([sys.executable, "-m", "pip", "install", "systemathics.apis"])
    
def regexreplace(path: str, pattern: str, replacement: str):
  with open(path,'r') as file:
      filedata = file.read()
      filedata = re.sub(pattern, replacement, filedata)
  with open(path,'w') as file:
      file.write(filedata)  
  
# Get token
thisdir = os.path.dirname(__file__)
import systemathics.apis.helpers.token_helpers as token_helpers
try:
  token = token_helpers.get_token()
  token = token.replace('Bearer ','')
except Exception as e:
  print("Could not get auth0 token: {}".format(e))
  
# overwrite env.ps1
envps1 = "{}/remoteaccess/env.ps1".format(thisdir)
print("Rewriting {}".format(envps1))
regexreplace(envps1, 'AUTH0_TOKEN=.*', 'AUTH0_TOKEN="{}"'.format(token))
  
# overwrite env.sh
envsh = "{}/remoteaccess/env.sh".format(thisdir)
print("Rewriting {}".format(envsh))
regexreplace(envsh, 'AUTH0_TOKEN=.*', 'AUTH0_TOKEN="{}"'.format(token))

# overwrite jupyter-lab-windows.cmd
jlwcmd = "{}/remoteaccess/jupyter-lab-windows.cmd".format(thisdir)
print("Rewriting {}".format(jlwcmd))
regexreplace(jlwcmd, 'AUTH0_TOKEN=.*', 'AUTH0_TOKEN="{}"'.format(token))

# Done
print()
print("AUTH0_TOKEN={}".format(token))
