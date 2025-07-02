#!/usr/bin/env python3
"""
Terminus Cross-Platform Installer
Automatically sets up Terminus on Windows, Linux, or macOS
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# ANSI color codes (basic, work on most terminals)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

def print_banner():
    """Display installation banner"""
    print(f"\n{CYAN}{'='*50}")
    print("   Terminus - System Software Manager")
    print("         Installation Script")
    print(f"{'='*50}{RESET}\n")

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"\n{RED}Error: Python 3.10 or higher is required!{RESET}")
        print(f"Your version: Python {version.major}.{version.minor}")
        print("\nPlease upgrade Python before continuing.")
        return False
    
    print(f"{GREEN}✓ Python version OK{RESET}")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print(f"{GREEN}✓ pip is installed{RESET}")
        return True
    except ImportError:
        print(f"{YELLOW}⚠ pip is not installed{RESET}")
        print("Attempting to install pip...")
        
        try:
            import ensurepip
            ensurepip.bootstrap()
            print(f"{GREEN}✓ pip installed successfully{RESET}")
            return True
        except:
            print(f"{RED}✗ Failed to install pip{RESET}")
            print("\nPlease install pip manually:")
            print("  curl https://bootstrap.pypa.io/get-pip.py | python3")
            return False

def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    
    packages = ['psutil', 'colorama']
    
    # Add Windows-specific packages
    if platform.system() == 'Windows':
        packages.extend(['pywin32', 'windows-curses'])
    
    for package in packages:
        print(f"Installing {package}...", end='', flush=True)
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '--quiet', '--upgrade', package
            ])
            print(f" {GREEN}✓{RESET}")
        except subprocess.CalledProcessError:
            print(f" {RED}✗{RESET}")
            print(f"\n{RED}Failed to install {package}{RESET}")
            print(f"Try manually: pip install {package}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    home = Path.home()
    terminus_dir = home / '.terminus'
    logs_dir = terminus_dir / 'logs'
    
    print("\nCreating directories...")
    
    try:
        terminus_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
        print(f"{GREEN}✓ Created {terminus_dir}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}✗ Failed to create directories: {e}{RESET}")
        return False

def make_executable():
    """Make launcher scripts executable on Unix-like systems"""
    if platform.system() in ['Linux', 'Darwin']:
        scripts = ['terminus.sh', 'terminus.py']
        
        for script in scripts:
            if os.path.exists(script):
                try:
                    os.chmod(script, 0o755)
                    print(f"{GREEN}✓ Made {script} executable{RESET}")
                except Exception as e:
                    print(f"{YELLOW}⚠ Could not make {script} executable: {e}{RESET}")

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if platform.system() != 'Windows':
        return
    
    try:
        import win32com.client
        
        desktop = Path.home() / 'Desktop'
        if not desktop.exists():
            return
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(desktop / "Terminus.lnk"))
        
        shortcut.Targetpath = str(Path.cwd() / 'terminus.bat')
        shortcut.WorkingDirectory = str(Path.cwd())
        shortcut.IconLocation = "cmd.exe"
        shortcut.Description = "Terminus - System Software Manager"
        shortcut.save()
        
        print(f"{GREEN}✓ Created desktop shortcut{RESET}")
    except:
        pass  # Silently skip if it fails

def verify_installation():
    """Verify that Terminus can be imported"""
    print("\nVerifying installation...")
    
    # Check if terminus.py exists
    if not os.path.exists('terminus.py'):
        print(f"{RED}✗ terminus.py not found!{RESET}")
        print("Make sure you're running this installer from the Terminus directory.")
        return False
    
    # Try to import required modules
    try:
        import psutil
        import colorama
        print(f"{GREEN}✓ All modules can be imported{RESET}")
        return True
    except ImportError as e:
        print(f"{RED}✗ Import error: {e}{RESET}")
        return False

def print_next_steps():
    """Print instructions for running Terminus"""
    print(f"\n{GREEN}{'='*50}")
    print("Installation Complete!")
    print(f"{'='*50}{RESET}\n")
    
    print("To run Terminus:")
    
    if platform.system() == 'Windows':
        print(f"\n{CYAN}Option 1: Double-click terminus.bat")
        print(f"Option 2: Run in PowerShell: .\\terminus.ps1")
        print(f"Option 3: Run directly: python terminus.py{RESET}")
        print(f"\n{YELLOW}Remember to run as Administrator for full functionality!{RESET}")
    else:
        print(f"\n{CYAN}Option 1: ./terminus.sh")
        print(f"Option 2: python3 terminus.py{RESET}")
        print(f"\n{YELLOW}Remember to use sudo for system operations!{RESET}")
    
    print(f"\n{WHITE}First time usage:")
    print("1. Start with 'Scan System Software' to see what's installed")
    print("2. Enable 'Dry Run Mode' in Settings to test safely")
    print("3. Always backup important data before removing software")
    print(f"\n{RED}⚠  Use with caution - this tool can permanently")
    print(f"   remove software and delete files!{RESET}")

def main():
    """Main installation process"""
    print_banner()
    
    # Detect OS
    os_name = platform.system()
    os_display = {
        'Windows': 'Windows',
        'Linux': 'Linux',
        'Darwin': 'macOS'
    }.get(os_name, 'Unknown')
    
    print(f"Detected OS: {BLUE}{os_display}{RESET}")
    print(f"Architecture: {platform.machine()}")
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print(f"\n{RED}Installation failed!{RESET}")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print(f"\n{YELLOW}Warning: Could not create all directories{RESET}")
    
    # Make scripts executable
    make_executable()
    
    # Create desktop shortcut (Windows)
    create_desktop_shortcut()
    
    # Verify installation
    if not verify_installation():
        print(f"\n{RED}Installation verification failed!{RESET}")
        print("Please check error messages above.")
        sys.exit(1)
    
    # Print success message and next steps
    print_next_steps()
    
    print(f"\n{GREEN}Happy system administration!{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Installation cancelled by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        print("Please report this issue.")
        sys.exit(1)