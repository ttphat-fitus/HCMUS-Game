@echo off
echo === Dino Run Python Game Setup (Windows) ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Running setup script...
python setup.py

if errorlevel 1 (
    echo.
    echo Setup failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Setup completed! 
echo.
echo To run the game:
echo 1. Double-click run_game.bat
echo    OR
echo 2. Open command prompt in this folder and run:
echo    venv\Scripts\activate
echo    python main.py
echo.
pause
