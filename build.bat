@echo off
echo Building Dino Run Game with Portable Path Support...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Cleaning previous builds...
echo.

REM Build the executable
echo Building executable with PyInstaller...
python -m PyInstaller Game.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===============================================
    echo BUILD SUCCESSFUL!
    echo ===============================================
    echo.
    echo Your executable is located at: dist\DinoRun.exe
    echo.
    echo PORTABLE FEATURES:
    echo - Runs from ANY directory location
    echo - All assets included internally
    echo - Save files created next to executable
    echo - No external dependencies required
    echo.
    echo You can now distribute the DinoRun.exe file!
    echo.
) else (
    echo.
    echo ===============================================
    echo BUILD FAILED!
    echo ===============================================
    echo.
    echo Please check the error messages above.
    echo If Python is not found, make sure Python is in your PATH
)

pause
