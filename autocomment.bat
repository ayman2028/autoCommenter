@echo off
REM Auto Commenter - Windows Batch Wrapper
REM This allows running the tool from anywhere
REM Usage: autocomment.bat <file> [output_file]

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if pipenv is installed
where pipenv >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Pipenv is not installed or not in PATH
    echo Install it with: pip install pipenv
    exit /b 1
)

REM Run the auto commenter with pipenv
cd /d "%SCRIPT_DIR%"
pipenv run python auto_commenter.py %*

endlocal
