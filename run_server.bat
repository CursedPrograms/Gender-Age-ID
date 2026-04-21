@echo off

set "VENV_DIR=venv"

rem 
if not exist "%VENV_DIR%" (
    rem 
    python -m venv "%VENV_DIR%"
)

rem 
call "%VENV_DIR%\Scripts\activate" && python app.py

rem 
pause
