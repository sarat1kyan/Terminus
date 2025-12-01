# Terminus Scripts Documentation

This document explains all scripts included with Terminus and their purposes.

## 📦 Installation Scripts

These scripts should be run **once** to set up Terminus on your system.

### `install.sh` (Linux/macOS)
- **Purpose:** Installs dependencies and sets up Terminus on Linux/macOS
- **Usage:** `chmod +x install.sh && ./install.sh`
- **What it does:**
  - Checks Python version (requires 3.10+)
  - Installs required Python packages (psutil, colorama)
  - Creates `~/.terminus` directory structure
  - Makes launcher scripts executable
  - Verifies installation

### `install.ps1` (Windows PowerShell)
- **Purpose:** Installs dependencies and sets up Terminus on Windows
- **Usage:** `.\install.ps1` (in PowerShell)
- **What it does:**
  - Checks Python version (requires 3.10+)
  - Installs required Python packages (psutil, colorama, pywin32, windows-curses)
  - Creates `%USERPROFILE%\.terminus` directory structure
  - Verifies installation
- **Note:** May require PowerShell execution policy change:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### `install.bat` (Windows Batch)
- **Purpose:** Alternative Windows installer using batch script
- **Usage:** Double-click or run `install.bat` from Command Prompt
- **What it does:** Same as `install.ps1` but uses batch commands
- **Advantage:** Works without PowerShell execution policy changes

### `install.py` (Cross-Platform)
- **Purpose:** Python-based installer that works on all platforms
- **Usage:** `python install.py` or `python3 install.py`
- **What it does:**
  - Cross-platform dependency installation
  - Creates necessary directories
  - Makes scripts executable (Unix-like systems)
  - Creates desktop shortcut (Windows, if possible)

**Recommendation:** Use platform-specific installers (`install.sh` or `install.ps1`) for better error handling and user experience.

---

## 🚀 Launcher Scripts

These scripts should be used **every time** you want to run Terminus. They handle dependency checks and provide better error messages.

### `terminus.sh` (Linux/macOS)
- **Purpose:** Launches Terminus with dependency checks
- **Usage:** `./terminus.sh` or `sudo ./terminus.sh` (for system operations)
- **What it does:**
  - Checks Python installation and version
  - Checks for required dependencies
  - Installs missing dependencies automatically
  - Checks for root privileges
  - Creates directories if needed
  - Launches `terminus.py`
- **Advantages:**
  - Automatic dependency installation
  - Better error messages
  - Privilege checking
  - UTF-8 encoding setup

### `terminus.ps1` (Windows PowerShell)
- **Purpose:** Launches Terminus with dependency checks on Windows
- **Usage:** `.\terminus.ps1` or right-click → "Run with PowerShell"
- **What it does:**
  - Checks Python installation and version
  - Checks for administrator privileges
  - Checks for required dependencies
  - Installs missing dependencies automatically
  - Creates directories if needed
  - Launches `terminus.py`
- **Advantages:**
  - Automatic dependency installation
  - Admin privilege checking
  - Better error messages
  - UTF-8 encoding setup

### `terminus.bat` (Windows Batch)
- **Purpose:** Simple batch launcher for Windows
- **Usage:** Double-click or run `terminus.bat` from Command Prompt
- **What it does:**
  - Checks Python version
  - Checks for administrator privileges
  - Installs missing dependencies
  - Launches `terminus.py`
- **Advantages:**
  - Works without PowerShell
  - Simple and fast
  - No execution policy issues

**Recommendation:** Always use launcher scripts instead of running `terminus.py` directly. They provide better error handling and automatic dependency management.

---

## 📝 Direct Execution

### `terminus.py` (Main Application)
- **Purpose:** The main Terminus application
- **Usage:** `python terminus.py` or `python3 terminus.py`
- **When to use:** Only if launcher scripts are not available
- **Note:** You must ensure all dependencies are installed manually

---

## 🔄 Script Workflow

### First Time Setup:
1. **Install:** Run the appropriate installer (`install.sh`, `install.ps1`, or `install.bat`)
2. **Verify:** Check that installation completed successfully
3. **Launch:** Use launcher scripts (`terminus.sh`, `terminus.ps1`, or `terminus.bat`)

### Daily Usage:
1. **Launch:** Use launcher scripts (they handle everything automatically)
2. **Run:** Terminus will check dependencies and launch

---

## ❓ Which Script Should I Use?

### For Installation:
- **Linux/macOS:** `install.sh` (recommended) or `install.py`
- **Windows:** `install.ps1` (recommended) or `install.bat` or `install.py`

### For Running Terminus:
- **Linux/macOS:** `terminus.sh` (always recommended)
- **Windows:** `terminus.ps1` (recommended) or `terminus.bat`
- **All Platforms:** `terminus.py` (only if launchers unavailable)

---

## 🛠️ Troubleshooting

### Script Not Executable (Linux/macOS)
```bash
chmod +x install.sh
chmod +x terminus.sh
```

### PowerShell Execution Policy (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Script Not Found
- Make sure you're in the Terminus directory
- Check that the script file exists
- Verify file permissions (Linux/macOS)

### Dependencies Not Installing
- Check internet connection
- Verify Python and pip are working: `python -m pip --version`
- Try manual installation: `pip install psutil colorama`

---

## 📋 Summary

| Script | Type | Platform | When to Use |
|--------|------|----------|-------------|
| `install.sh` | Installer | Linux/macOS | First-time setup |
| `install.ps1` | Installer | Windows | First-time setup (PowerShell) |
| `install.bat` | Installer | Windows | First-time setup (Batch) |
| `install.py` | Installer | All | Cross-platform installer |
| `terminus.sh` | Launcher | Linux/macOS | Every time you run Terminus |
| `terminus.ps1` | Launcher | Windows | Every time you run Terminus (PowerShell) |
| `terminus.bat` | Launcher | Windows | Every time you run Terminus (Batch) |
| `terminus.py` | Application | All | Direct execution (not recommended) |

---

**All scripts are needed and serve specific purposes. Use launcher scripts for daily use and installer scripts for initial setup.**

