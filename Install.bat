@echo off
@title Installing

echo - Installing Python3
@echo on
winget install python3
@echo off

echo - Updating Pip
@echo on
python -m pip install --upgrade pip
@echo off

echo - Create Virtual Environment and Activating it
@echo on
python -m venv %CD%/venv/
call %CD%/venv/Scripts/activate.bat
@echo off

echo - Installing Dependencies
@echo on
%CD%/venv/Scripts/pip3 install -r %CD%/requirements.txt
@echo off

echo - Deactivating Virtual Environment
@echo on
call %CD%/venv/Scripts/deactivate.bat
@echo off

echo - Done