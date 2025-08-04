@echo off
setlocal
echo Starting Billing Management System...
echo.

:: Get the directory of this .bat file
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

:: Check if virtual environment exists
if not exist ".venv\" (
    echo [ERROR] Virtual environment not found at: %PROJECT_DIR%.venv
    echo Run: python -m venv .venv
    pause
    exit /b 1
)

:: Activate virtual environment
call ".venv\Scripts\activate.bat"

:: Check server
echo Checking server status...
python checkServer.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Server check failed. Please check configuration.
    pause
    exit /b 1
)

:: Launch GUI app silently (no CMD window)
echo Launching Billing Management System...
start "" ".venv\Scripts\pythonw.exe" BillingManagementSystem.py

endlocal
exit
