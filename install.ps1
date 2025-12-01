# Terminus Installation Script for Windows
# PowerShell script to install dependencies and set up Terminus

# Set error handling
$ErrorActionPreference = "Stop"

# Colors
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

# Banner
Clear-Host
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" "Cyan"
Write-ColorOutput "║                                                            ║" "Cyan"
Write-ColorOutput "║     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗     ║" "Cyan"
Write-ColorOutput "║     ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║     ║" "Cyan"
Write-ColorOutput "║        ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║     ║" "Cyan"
Write-ColorOutput "║        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║     ║" "Cyan"
Write-ColorOutput "║        ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║     ║" "Cyan"
Write-ColorOutput "║        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝     ║" "Cyan"
Write-ColorOutput "║                                                            ║" "Cyan"
Write-ColorOutput "║           Installation Script v5.0 ULTIMATE                ║" "Cyan"
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" "Cyan"
Write-Host ""

# Check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check Python
Write-ColorOutput "Checking Python installation..." "Yellow"

try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $majorVersion = [int]$matches[1]
        $minorVersion = [int]$matches[2]
        
        if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 10)) {
            Write-ColorOutput "✗ Python 3.10 or higher is required!" "Red"
            Write-ColorOutput "  Your version: Python $majorVersion.$minorVersion" "Red"
            Write-ColorOutput "  Download from: https://www.python.org/downloads/" "Yellow"
            exit 1
        }
        
        Write-ColorOutput "✓ Found: $pythonVersion" "Green"
    }
} catch {
    Write-ColorOutput "✗ Python is not installed or not in PATH!" "Red"
    Write-ColorOutput "  Download from: https://www.python.org/downloads/" "Yellow"
    Write-ColorOutput "  Make sure to check 'Add Python to PATH' during installation" "Yellow"
    exit 1
}

Write-Host ""

# Check pip
Write-ColorOutput "Checking pip..." "Yellow"
try {
    python -m pip --version | Out-Null
    Write-ColorOutput "✓ pip found" "Green"
} catch {
    Write-ColorOutput "✗ pip not found" "Red"
    Write-ColorOutput "  Installing pip..." "Yellow"
    python -m ensurepip --upgrade
    Write-ColorOutput "✓ pip installed" "Green"
}

Write-Host ""

# Install dependencies
Write-ColorOutput "Installing Python dependencies..." "Yellow"
Write-Host ""

$requiredPackages = @("psutil", "colorama", "pywin32", "windows-curses")
$installed = 0
$failed = 0

foreach ($package in $requiredPackages) {
    Write-Host "  Installing $package... " -NoNewline
    
    try {
        python -m pip install --upgrade --quiet $package 2>&1 | Out-Null
        Write-ColorOutput "✓" "Green"
        $installed++
    } catch {
        Write-ColorOutput "✗" "Red"
        $failed++
    }
}

Write-Host ""

if ($failed -gt 0) {
    Write-ColorOutput "✗ Failed to install some packages" "Red"
    Write-ColorOutput "Try installing manually:" "Yellow"
    Write-Host "  python -m pip install psutil colorama pywin32 windows-curses"
    exit 1
}

Write-ColorOutput "✓ All dependencies installed successfully" "Green"
Write-Host ""

# Create directories
Write-ColorOutput "Creating Terminus directories..." "Yellow"
$terminusDir = Join-Path $env:USERPROFILE ".terminus"
$logsDir = Join-Path $terminusDir "logs"

if (-not (Test-Path $terminusDir)) {
    New-Item -ItemType Directory -Path $terminusDir -Force | Out-Null
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
    Write-ColorOutput "✓ Created $terminusDir" "Green"
} else {
    Write-ColorOutput "✓ Directories already exist" "Green"
}

Write-Host ""

# Verify installation
Write-ColorOutput "Verifying installation..." "Yellow"

if (-not (Test-Path "terminus.py")) {
    Write-ColorOutput "✗ terminus.py not found!" "Red"
    Write-ColorOutput "Make sure you're running this script from the Terminus directory." "Yellow"
    exit 1
}

# Test imports
try {
    python -c "import psutil, colorama, win32api" 2>&1 | Out-Null
    Write-ColorOutput "✓ All modules imported successfully" "Green"
} catch {
    Write-ColorOutput "✗ Module import failed" "Red"
    exit 1
}

Write-Host ""

# Success message
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" "Green"
Write-ColorOutput "║                                                            ║" "Green"
Write-ColorOutput "║           Installation Complete! ✓                        ║" "Green"
Write-ColorOutput "║                                                            ║" "Green"
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" "Green"
Write-Host ""

Write-ColorOutput "To run Terminus:" "Cyan"
Write-Host "  .\terminus.ps1        # Recommended (handles dependencies)"
Write-Host "  .\terminus.bat        # Alternative launcher"
Write-Host "  python terminus.py    # Direct execution"
Write-Host ""

if (-not (Test-Administrator)) {
    Write-ColorOutput "⚠ Note: Some features require Administrator privileges" "Yellow"
    Write-Host "  Right-click and select 'Run as Administrator'" "White"
    Write-Host ""
}

Write-ColorOutput "First time usage tips:" "Yellow"
Write-Host "  1. Start with 'Scan System Software' to see what's installed"
Write-Host "  2. Enable 'Dry Run Mode' in Settings to test safely"
Write-Host "  3. Always backup important data before removing software"
Write-Host "  4. Test in a virtual machine first!"
Write-Host ""

Write-ColorOutput "⚠ WARNING: This tool can permanently remove software and files!" "Red"
Write-Host ""

