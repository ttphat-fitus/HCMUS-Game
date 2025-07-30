@echo off
echo Starting Dino Run Game...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup.bat first to set up the game.
    pause
    exit /b 1
)

REM Activate virtual environment and run game
call venv\Scripts\activate.bat
python main.py

if errorlevel 1 (
    echo.
    echo Game exited with an error.
    pause
)
