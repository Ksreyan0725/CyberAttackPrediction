@echo off
:: SESSION PERSISTENCE HARDENING: No setlocal here so venv stays active after Ctrl+C.
echo Starting the Web App (Main.py) using the .venv...

:: Venv Guard: Avoid redundant activation if already in session
if defined VIRTUAL_ENV (
    echo [Session] Active environment detected. Skipping activation...
) else (
    if exist "..\.venv\Scripts\activate.bat" (
        call ..\.venv\Scripts\activate.bat
    ) else (
        echo [Error] Virtual environment not found in root!
        pause
        exit /b
    )
)

:: Secure Workspace Shift
pushd "%~dp0..\CyberAttackPrediction"

:: Heartbeat-Aware Smart Launch:
:: No .browser_lock needed anymore! The server (Main.py) will now dynamically 
:: check for open pulses before launching a new tab.
:: This is a much smoother and more professional experience.

:RESTART_LOOP
cls
echo ==========================================
echo    CyberShield AI Dashboard - STARTING
echo ==========================================

:: Run the server (let Main.py handle the smart browser launch)
python Main.py

echo.
echo ==========================================
echo    SERVER STOPPED OR CRASHED!
echo    Press any key to RESTART the server...
echo    Close this window to quit.
echo ==========================================
pause > nul
goto RESTART_LOOP
