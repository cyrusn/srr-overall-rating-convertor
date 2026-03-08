@echo off
setlocal
cd /d %~dp0\v2

if exist ".\venv\Scripts\python.exe" (
    .\venv\Scripts\python.exe main.py %*
) else (
    echo Error: Virtual environment not found in v2\venv.
    echo Please run the setup steps in v2\README.md first.
    pause
    exit /b 1
)

echo.
echo Process Complete.
pause
