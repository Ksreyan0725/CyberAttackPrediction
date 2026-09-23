@echo off
:: SESSION PERSISTENCE HARDENING: No setlocal here so venv stays active after Ctrl+C.
echo Starting Jupyter Notebook using the .venv...

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

:: Launch Jupyter in Chrome Incognito with Robust Shell Execution
:: Using 'cmd /c start' allows Windows to find Chrome via Registry even if not in PATH.
jupyter notebook --browser="cmd /c start chrome --incognito %%s"

:: Restoration: Restore directory after closing Jupyter
popd
pause
