@echo off
setlocal enabledelayedexpansion
cd "E:\Billing-Software\"

echo Checking server status... (waiting up to 60s)

for /f "delims=" %%i in ('C:\Users\nebin\AppData\Local\Programs\Python\Python313\python.exe "E:\Billing-Software\checkServer.py"') do set status=%%i

echo Status: !status!

if /i "!status!"=="CONNECTED" (
    echo Server connected.
    timeout /t 4 >nul
    start "" "C:/Users/nebin/AppData/Local/Programs/Python/Python313/pythonw.exe" "E:\Billing-Software\BillingManagementSystem.py"
) else (
    echo Server not connected. Please try again later.
    pause
)

endlocal    
