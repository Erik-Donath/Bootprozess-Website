@echo off
@title Webserver - Bootprozess
cd ..

if not exist %CD%/venv/ call Install.bat

@echo off
call %CD%/venv/Scripts/activate.bat
%CD%/venv/Scripts/python.exe %CD%/run.py
call %CD%/venv/Scripts/deactivate.bat

echo Program stopped
pause
exit
