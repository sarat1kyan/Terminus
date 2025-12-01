@echo off
REM Terminus Installation Script for Windows
REM Batch script to install dependencies and set up Terminus

title Terminus Installation
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗     ║
echo ║     ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║     ║
echo ║        ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║     ║
echo ║        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║     ║
echo ║        ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║     ║
echo ║        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝     ║
echo ║                                                            ║
echo ║           Installation Script v5.0 ULTIMATE                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ✗ Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

python --version
echo ✓ Python found
echo.

REM Check pip
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    python -m ensurepip --upgrade
)
echo ✓ pip found
echo.

REM Install dependencies
echo Installing Python dependencies...
echo.

python -m pip install --upgrade --quiet psutil
if errorlevel 1 (
    echo ✗ Failed to install psutil
    goto :error
) else (
    echo ✓ psutil installed
)

python -m pip install --upgrade --quiet colorama
if errorlevel 1 (
    echo ✗ Failed to install colorama
    goto :error
) else (
    echo ✓ colorama installed
)

python -m pip install --upgrade --quiet pywin32
if errorlevel 1 (
    echo ✗ Failed to install pywin32
    goto :error
) else (
    echo ✓ pywin32 installed
)

python -m pip install --upgrade --quiet windows-curses
if errorlevel 1 (
    echo ✗ Failed to install windows-curses
    goto :error
) else (
    echo ✓ windows-curses installed
)

echo.
echo ✓ All dependencies installed successfully
echo.

REM Create directories
echo Creating Terminus directories...
if not exist "%USERPROFILE%\.terminus" (
    mkdir "%USERPROFILE%\.terminus"
    mkdir "%USERPROFILE%\.terminus\logs"
    echo ✓ Created directories
) else (
    echo ✓ Directories already exist
)
echo.

REM Verify installation
echo Verifying installation...
if not exist "terminus.py" (
    color 0C
    echo.
    echo ✗ terminus.py not found!
    echo Make sure you're running this script from the Terminus directory.
    echo.
    pause
    exit /b 1
)

python -c "import psutil, colorama, win32api" >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ✗ Module import failed
    goto :error
) else (
    echo ✓ All modules imported successfully
)
echo.

REM Success
color 0A
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           Installation Complete! ✓                        ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo To run Terminus:
echo   terminus.bat        # Recommended launcher
echo   terminus.ps1        # PowerShell launcher
echo   python terminus.py  # Direct execution
echo.
echo ⚠ Note: Some features require Administrator privileges
echo   Right-click and select "Run as Administrator"
echo.
echo First time usage tips:
echo   1. Start with 'Scan System Software'
echo   2. Enable 'Dry Run Mode' in Settings
echo   3. Always backup important data
echo   4. Test in a virtual machine first!
echo.
echo ⚠ WARNING: This tool can permanently remove software and files!
echo.
pause
exit /b 0

:error
color 0C
echo.
echo Installation failed!
echo.
pause
exit /b 1

