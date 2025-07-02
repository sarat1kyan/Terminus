@echo off
title Terminus - System Software Manager
color 0A

echo.
echo ========================================
echo    Terminus - System Software Manager
echo           Windows Launcher
echo ========================================
echo.

:: Check Python version
echo Checking Python installation...
python --version 2>NUL | findstr /C:"Python 3.1" >NUL
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Python 3.10 or higher is required!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Display Python version
python --version

:: Check admin rights
echo.
echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    color 0E
    echo.
    echo WARNING: Not running as Administrator!
    echo.
    echo Some features will be limited without admin rights:
    echo  - Cannot remove system software
    echo  - Cannot clean registry
    echo  - Cannot modify protected files
    echo.
    echo To run as Administrator:
    echo  1. Right-click on terminus.bat
    echo  2. Select "Run as administrator"
    echo.
    echo Press any key to continue with limited privileges...
    pause >nul
    echo.
)

:: Check and install dependencies
echo Checking dependencies...
python -c "import psutil" 2>NUL
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    echo This may take a few minutes on first run...
    echo.
    
    :: Upgrade pip first
    python -m pip install --upgrade pip
    
    :: Install dependencies
    echo Installing psutil...
    pip install psutil
    
    echo Installing colorama...
    pip install colorama
    
    echo Installing pywin32...
    pip install pywin32
    
    echo Installing windows-curses...
    pip install windows-curses
    
    echo.
    echo Dependencies installed successfully!
    echo.
)

:: Set console code page to UTF-8 for better character support
chcp 65001 >nul 2>&1

:: Clear screen before starting
cls

:: Run Terminus
echo Starting Terminus...
echo.
python terminus.py %*

:: Check if Terminus exited with error
if errorlevel 1 (
    color 0C
    echo.
    echo Terminus exited with an error.
    echo Check the logs in %USERPROFILE%\.terminus\logs\
    echo.
)

:: Pause to see any final messages
echo.
echo Press any key to exit...
pause >nul