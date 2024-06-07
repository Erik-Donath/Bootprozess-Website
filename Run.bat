@echo off
@title Webserver - Bootprozess

if not exist %CD%/venv/ call Install.bat

call %CD%/venv/Scripts/activate.bat
%CD%/venv/Scripts/python.exe %CD%/server.py
call %CD%/venv/Scripts/deactivate.bat

echo Program stopped
pause
exit
