# Terminus - System Software Manager
# PowerShell Launcher Script
#
# To enable PowerShell scripts:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Set console colors
$Host.UI.RawUI.WindowTitle = "Terminus - System Software Manager"
$Host.UI.RawUI.BackgroundColor = "Black"
Clear-Host

# Banner
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Terminus - System Software Manager   " -ForegroundColor Cyan
Write-Host "        PowerShell Launcher            " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if running as admin
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $majorVersion = [int]$matches[1]
        $minorVersion = [int]$matches[2]
        
        Write-Host "Found: $pythonVersion" -ForegroundColor Green
        
        if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 10)) {
            Write-Host ""
            Write-Host "ERROR: Python 3.10 or higher is required!" -ForegroundColor Red
            Write-Host "Your version: Python $majorVersion.$minorVersion" -ForegroundColor Red
            Write-Host ""
            Write-Host "Download Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
            Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10 or higher from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "During installation, make sure to:" -ForegroundColor Yellow
    Write-Host "  ✓ Check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  ✓ Check 'Install pip'" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# Check administrator privileges
Write-Host "Checking administrator privileges..." -ForegroundColor Yellow

if (Test-Administrator) {
    Write-Host "✓ Running as Administrator" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠ WARNING: Not running as Administrator!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Limited functionality without admin rights:" -ForegroundColor White
    Write-Host "  - Cannot remove system software" -ForegroundColor Gray
    Write-Host "  - Cannot clean registry" -ForegroundColor Gray
    Write-Host "  - Cannot modify protected files" -ForegroundColor Gray
    Write-Host "  - Cannot create system restore points" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To run as Administrator:" -ForegroundColor Yellow
    Write-Host "  1. Right-click on terminus.ps1" -ForegroundColor White
    Write-Host "  2. Select 'Run with PowerShell' while holding Shift+Ctrl" -ForegroundColor White
    Write-Host "  OR" -ForegroundColor Gray
    Write-Host "  1. Open PowerShell as Administrator" -ForegroundColor White
    Write-Host "  2. Navigate to Terminus directory" -ForegroundColor White
    Write-Host "  3. Run: .\terminus.ps1" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "Continue with limited privileges? (Y/N)"
    if ($response -ne "Y" -and $response -ne "y") {
        exit 0
    }
}

Write-Host ""

# Function to check if Python module is installed
function Test-PythonModule {
    param($ModuleName)
    
    $result = python -c "import $ModuleName" 2>&1
    return $LASTEXITCODE -eq 0
}

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$requiredModules = @("psutil", "colorama")
$windowsModules = @("pywin32", "windows-curses")
$missingModules = @()

foreach ($module in $requiredModules) {
    if (-not (Test-PythonModule $module)) {
        $missingModules += $module
    }
}

# Check Windows-specific modules
foreach ($module in $windowsModules) {
    $moduleName = $module
    if ($module -eq "pywin32") {
        $moduleName = "win32api"  # Test import name for pywin32
    }
    if (-not (Test-PythonModule $moduleName)) {
        $missingModules += $module
    }
}

# Install missing dependencies
if ($missingModules.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing dependencies: $($missingModules -join ', ')" -ForegroundColor Yellow
    Write-Host "Installing required packages..." -ForegroundColor White
    Write-Host ""
    
    # Upgrade pip first
    Write-Host "Upgrading pip..." -ForegroundColor Gray
    python -m pip install --upgrade pip
    
    # Install each missing module
    foreach ($module in $missingModules) {
        Write-Host "Installing $module..." -ForegroundColor Gray
        python -m pip install $module
        
        # Verify installation
        $testModule = $module
        if ($module -eq "pywin32") {
            $testModule = "win32api"
        }
        
        if (Test-PythonModule $testModule) {
            Write-Host "✓ $module installed successfully" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to install $module" -ForegroundColor Red
            Write-Host ""
            Write-Host "Try installing manually:" -ForegroundColor Yellow
            Write-Host "  python -m pip install $module" -ForegroundColor White
            Write-Host ""
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host "All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✓ All dependencies are installed" -ForegroundColor Green
}

Write-Host ""

# Create Terminus directory if it doesn't exist
$terminusDir = Join-Path $env:USERPROFILE ".terminus"
$logsDir = Join-Path $terminusDir "logs"

if (-not (Test-Path $terminusDir)) {
    Write-Host "Creating Terminus directories..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $terminusDir -Force | Out-Null
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
    Write-Host "✓ Created $terminusDir" -ForegroundColor Green
}

# Check if terminus.py exists
if (-not (Test-Path "terminus.py")) {
    Write-Host ""
    Write-Host "ERROR: terminus.py not found in current directory!" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the Terminus directory." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Set console to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "Starting Terminus..." -ForegroundColor Green
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Run Terminus with all passed arguments
$arguments = $args -join " "
if ($arguments) {
    python terminus.py $arguments
} else {
    python terminus.py
}

$exitCode = $LASTEXITCODE

# Check exit status
Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "Terminus exited successfully" -ForegroundColor Green
} else {
    Write-Host "Terminus exited with error code: $exitCode" -ForegroundColor Red
    Write-Host "Check logs in: $logsDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")