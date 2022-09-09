@echo off

REM Use values from your dashboard token
set CLIENT_ID=please-fill-in-here
set CLIENT_SECRET=please-fill-in-here
 
REM Launches Jupyter lab from the python notebooks folder
jupyter-lab.exe ..\python
