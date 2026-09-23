@echo off
setlocal
echo Launching the CyberShield AI Hub...

:: Run the launcher using current environment (global or already active venv)
python ..\launcher.py

:: If it crashes, keep the window open
if %ERRORLEVEL% neq 0 (
    echo.
    echo ==========================================
    echo    LAUNCHER STOPPED OR CRASHED!
    echo    Press any key to exit...
    echo ==========================================
    pause > nul
)
