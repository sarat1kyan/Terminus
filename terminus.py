#!/usr/bin/env python3
"""
Terminus - The Ultimate System Cleaner
========================================
Version 4.0
Build 475326
Built with Python 3.10+
Copyright (c) 2023-2025 Mher Saratikyan
Licensed under the GNU General Public License v3.0
A powerful tool for system administrators to manage and remove software
"""

import os
import sys
import time
import json
import shutil
import platform
import subprocess
import logging
import hashlib
import tempfile
import stat
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import threading
import queue
import ctypes
import struct

# Third-party imports
try:
    import psutil
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
except ImportError as e:
    print(f"Missing required module: {e}")
    print("Please install: pip install psutil colorama")
    sys.exit(1)

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import winreg
        import win32api
        import win32security
        import win32con
        import win32file
        import win32process
        import pywintypes
        from ctypes import wintypes
        import msvcrt  # For Windows keyboard input
    except ImportError:
        print("Windows modules not found. Install: pip install pywin32")
        sys.exit(1)
else:
    import termios
    import tty
    import select

# Constants
APP_NAME = "Terminus"
VERSION = "5.0 ULTIMATE"
LOG_DIR = Path.home() / ".terminus" / "logs"
CONFIG_DIR = Path.home() / ".terminus"
SECURE_DELETE_PASSES = 7  # Enhanced from 3 to 7 passes

# Enhanced ASCII Art Logo with better styling
LOGO = f"""
{Fore.CYAN}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  {Fore.MAGENTA}████████╗{Fore.CYAN}███████╗{Fore.MAGENTA}██████╗{Fore.CYAN} ███╗   ███╗{Fore.MAGENTA}██╗{Fore.CYAN}███╗   ██╗{Fore.MAGENTA}██╗{Fore.CYAN}   ██╗{Fore.MAGENTA}██╗{Fore.CYAN}   ██╗{Fore.MAGENTA}███████╗{Fore.CYAN}    ║
║  {Fore.MAGENTA}╚══██╔══╝{Fore.CYAN}██╔════╝{Fore.MAGENTA}██╔══██╗{Fore.CYAN}████╗ ████║{Fore.MAGENTA}██║{Fore.CYAN}████╗  ██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}██╔════╝{Fore.CYAN}    ║
║     {Fore.MAGENTA}██║{Fore.CYAN}   █████╗  {Fore.MAGENTA}██████╔╝{Fore.CYAN}██╔████╔██║{Fore.MAGENTA}██║{Fore.CYAN}██╔██╗ ██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}███████╗{Fore.CYAN}    ║
║     {Fore.MAGENTA}██║{Fore.CYAN}   ██╔══╝  {Fore.MAGENTA}██╔══██╗{Fore.CYAN}██║╚██╔╝██║{Fore.MAGENTA}██║{Fore.CYAN}██║╚██╗██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}██║{Fore.CYAN}   ██║{Fore.MAGENTA}╚════██║{Fore.CYAN}    ║
║     {Fore.MAGENTA}██║{Fore.CYAN}   ███████╗{Fore.MAGENTA}██║  ██║{Fore.CYAN}██║ ╚═╝ ██║{Fore.MAGENTA}██║{Fore.CYAN}██║ ╚████║{Fore.MAGENTA}╚██████╔╝{Fore.MAGENTA}╚██████╔╝{Fore.MAGENTA}███████║{Fore.CYAN}    ║
║     {Fore.MAGENTA}╚═╝{Fore.CYAN}   ╚══════╝{Fore.MAGENTA}╚═╝  ╚═╝{Fore.CYAN}╚═╝     ╚═╝{Fore.MAGENTA}╚═╝{Fore.CYAN}╚═╝  ╚═══╝{Fore.MAGENTA} ╚═════╝ {Fore.MAGENTA} ╚═════╝ {Fore.MAGENTA}╚══════╝{Fore.CYAN}    ║
║                                                                           ║
║  {Fore.YELLOW}╔═══════════════════════════════════════════════════════════════════╗{Fore.CYAN}    ║
║  {Fore.YELLOW}║{Fore.GREEN}  ⚡ ULTIMATE SYSTEM CLEANER - REMOVES EVERYTHING ⚡{Fore.YELLOW}      ║{Fore.CYAN}    ║
║  {Fore.YELLOW}║{Fore.RED}  Version {VERSION} - Cross-Platform Power Tool{Fore.YELLOW}            ║{Fore.CYAN}    ║
║  {Fore.YELLOW}╚═══════════════════════════════════════════════════════════════════╝{Fore.CYAN}    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
# Initialize logging

class Logger:
    """Enhanced logging with file and console output"""
    def __init__(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.log_file = LOG_DIR / f"terminus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)

class UIRenderer:
    """Beautiful terminal UI rendering utilities"""
    
    # Box drawing characters
    BOX_H = "═"
    BOX_V = "║"
    BOX_TL = "╔"
    BOX_TR = "╗"
    BOX_BL = "╚"
    BOX_BR = "╝"
    BOX_TJ = "╦"
    BOX_BJ = "╩"
    BOX_LJ = "╠"
    BOX_RJ = "╣"
    BOX_C = "╬"
    
    @staticmethod
    def draw_box(width: int, height: int, title: str = "", color: str = Fore.CYAN) -> str:
        """Draw a beautiful box with optional title"""
        lines = []
        top = f"{color}{UIRenderer.BOX_TL}{UIRenderer.BOX_H * (width - 2)}{UIRenderer.BOX_TR}{Style.RESET_ALL}"
        
        if title:
            title_line = f"{color}{UIRenderer.BOX_V}{Style.RESET_ALL} {Fore.YELLOW}{Style.BRIGHT}{title}{Style.RESET_ALL} "
            title_padding = width - len(title) - 4
            if title_padding > 0:
                title_line += " " * title_padding
            title_line += f"{color}{UIRenderer.BOX_V}{Style.RESET_ALL}"
            lines.append(top)
            lines.append(title_line)
            lines.append(f"{color}{UIRenderer.BOX_LJ}{UIRenderer.BOX_H * (width - 2)}{UIRenderer.BOX_RJ}{Style.RESET_ALL}")
        else:
            lines.append(top)
        
        for _ in range(height - 2):
            lines.append(f"{color}{UIRenderer.BOX_V}{Style.RESET_ALL}" + " " * (width - 2) + f"{color}{UIRenderer.BOX_V}{Style.RESET_ALL}")
        
        lines.append(f"{color}{UIRenderer.BOX_BL}{UIRenderer.BOX_H * (width - 2)}{UIRenderer.BOX_BR}{Style.RESET_ALL}")
        return "\n".join(lines)
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 50, label: str = "") -> str:
        """Create a beautiful progress bar"""
        if total == 0:
            percent = 0
        else:
            percent = min(100, int((current / total) * 100))
        
        filled = int(width * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (width - filled)
        
        result = f"{Fore.CYAN}[{Fore.GREEN}{bar}{Fore.CYAN}]{Style.RESET_ALL} {Fore.YELLOW}{percent:3d}%{Style.RESET_ALL}"
        if label:
            result += f" {Fore.WHITE}{label}{Style.RESET_ALL}"
        return result
    
    @staticmethod
    def print_header(text: str, width: int = 80):
        """Print a beautiful header"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'═' * width}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{text.center(width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'═' * width}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_success(msg: str):
        """Print success message"""
        print(f"{Fore.GREEN}{Style.BRIGHT}✓{Style.RESET_ALL} {Fore.GREEN}{msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(msg: str):
        """Print error message"""
        print(f"{Fore.RED}{Style.BRIGHT}✗{Style.RESET_ALL} {Fore.RED}{msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(msg: str):
        """Print warning message"""
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠{Style.RESET_ALL} {Fore.YELLOW}{msg}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(msg: str):
        """Print info message"""
        print(f"{Fore.CYAN}{Style.BRIGHT}ℹ{Style.RESET_ALL} {Fore.CYAN}{msg}{Style.RESET_ALL}")

class PermissionManager:
    """Aggressive permission management for file/directory access"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
    
    def force_take_ownership(self, path: str):
        """Force take ownership of a file or directory"""
        self.logger.info(f"Taking ownership of: {path}")
        
        if self.system == "Windows":
            self._windows_take_ownership(path)
        else:
            self._unix_take_ownership(path)
    
    def _windows_take_ownership(self, path: str):
        """Windows: Take ownership using Windows API"""
        try:
            # Get current user's SID
            username = win32api.GetUserName()
            domain = win32api.GetDomainName()
            
            # Get the SID
            sid, domain, type = win32security.LookupAccountName(domain, username)
            
            # Open the file/directory with WRITE_OWNER access
            if os.path.isdir(path):
                handle = win32file.CreateFile(
                    path,
                    win32con.WRITE_OWNER,
                    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                    None,
                    win32con.OPEN_EXISTING,
                    win32con.FILE_FLAG_BACKUP_SEMANTICS,
                    None
                )
            else:
                handle = win32file.CreateFile(
                    path,
                    win32con.WRITE_OWNER,
                    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                    None,
                    win32con.OPEN_EXISTING,
                    win32con.FILE_ATTRIBUTE_NORMAL,
                    None
                )
            
            # Set owner
            win32security.SetSecurityInfo(
                handle,
                win32security.SE_FILE_OBJECT,
                win32security.OWNER_SECURITY_INFORMATION,
                sid,
                None,
                None,
                None
            )
            
            win32api.CloseHandle(handle)
            
            # Now grant full control
            self._windows_grant_full_control(path, username)
            
            self.logger.info(f"Successfully took ownership of: {path}")
            
        except Exception as e:
            self.logger.error(f"Failed to take ownership: {e}")
            # Try alternative method
            self._windows_takeown_cmd(path)
    
    def _windows_takeown_cmd(self, path: str):
        """Fallback: Use takeown and icacls commands"""
        try:
            # Take ownership
            subprocess.run(
                ["takeown", "/f", path, "/r", "/d", "y"],
                capture_output=True,
                shell=True,
                check=True
            )
            
            # Grant full permissions
            subprocess.run(
                ["icacls", path, "/grant", f"{os.environ.get('USERNAME')}:F", "/t", "/c", "/q"],
                capture_output=True,
                shell=True,
                check=True
            )
            
            self.logger.info(f"Ownership taken via commands: {path}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
    
    def _windows_grant_full_control(self, path: str, username: str):
        """Grant full control to user"""
        try:
            # Get security descriptor
            sd = win32security.GetFileSecurity(
                path,
                win32security.DACL_SECURITY_INFORMATION
            )
            
            # Get DACL
            dacl = sd.GetSecurityDescriptorDacl()
            
            # Create new ACE with full control
            user_sid, domain, type = win32security.LookupAccountName("", username)
            
            # Add full control ACE
            dacl.AddAccessAllowedAce(
                win32security.ACL_REVISION,
                win32con.GENERIC_ALL,
                user_sid
            )
            
            # Set the new DACL
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(
                path,
                win32security.DACL_SECURITY_INFORMATION,
                sd
            )
            
        except Exception as e:
            self.logger.error(f"Failed to grant permissions: {e}")
    
    def _unix_take_ownership(self, path: str):
        """Unix: Take ownership using system commands"""
        try:
            # Try to change ownership
            if os.geteuid() == 0:  # Running as root
                # Change to root ownership
                os.chown(path, 0, 0)
                
                # Set full permissions
                if os.path.isdir(path):
                    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                else:
                    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                
                self.logger.info(f"Ownership changed: {path}")
            else:
                # Try with sudo
                subprocess.run(
                    ["sudo", "chown", f"{os.getuid()}:{os.getgid()}", path],
                    check=True
                )
                subprocess.run(
                    ["sudo", "chmod", "777", path],
                    check=True
                )
                
        except Exception as e:
            self.logger.error(f"Failed to change ownership: {e}")
    
    def unlock_file(self, path: str):
        """Unlock a file by killing processes that hold it"""
        self.logger.info(f"Unlocking file: {path}")
        
        # Find processes using the file
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for file in proc.open_files():
                    if path in file.path:
                        self.logger.warning(f"Terminating process {proc.info['name']} (PID: {proc.info['pid']}) holding file")
                        proc.terminate()
                        proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Windows specific: unlock with handle
        if self.system == "Windows":
            self._windows_unlock_file(path)
    
    def _windows_unlock_file(self, path: str):
        """Windows: Force unlock file"""
        try:
            # Use handle utility if available
            handle_exe = "handle.exe"  # Sysinternals tool
            if shutil.which(handle_exe):
                result = subprocess.run(
                    [handle_exe, "-c", path, "-y"],
                    capture_output=True,
                    text=True
                )
                self.logger.info("File unlocked with handle.exe")
        except:
            pass

class SystemScanner:
    """Enhanced system scanner that properly detects installed software - ULTRA COMPREHENSIVE"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
        self.system_version = platform.release()
        self.architecture = platform.machine()
        self.software_cache = []
        
        # Enhanced OS detection
        if self.system == "Linux":
            try:
                # Try to detect Linux distribution
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release", "r") as f:
                        for line in f:
                            if line.startswith("ID="):
                                self.distribution = line.split("=")[1].strip().strip('"')
                                break
                else:
                    self.distribution = "Unknown"
            except:
                self.distribution = "Unknown"
        elif self.system == "Darwin":
            try:
                # Get macOS version
                result = subprocess.run(["sw_vers", "-productVersion"], 
                                      capture_output=True, text=True)
                self.macos_version = result.stdout.strip()
            except:
                self.macos_version = "Unknown"
        
    def scan_installed_software(self) -> List[Dict]:
        """Scan for all installed software - FIXED to show actual software"""
        self.logger.info("Starting comprehensive system software scan...")
        software_list = []
        
        # First scan actual installed software
        if self.system == "Windows":
            software_list.extend(self._scan_windows_software())
            software_list.extend(self._scan_windows_store_apps())
        elif self.system == "Linux":
            software_list.extend(self._scan_linux_software())
        elif self.system == "Darwin":
            software_list.extend(self._scan_macos_software())
        
        # Then add running processes as a separate category
        processes = self._scan_running_processes()
        
        # Cache results
        self.software_cache = software_list + processes
        
        self.logger.info(f"Found {len(software_list)} software packages and {len(processes)} processes")
        return self.software_cache
    
    def _scan_windows_software(self) -> List[Dict]:
        """Enhanced Windows software scanning"""
        software = []
        
        # All registry paths to check
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Classes\Installer\Products"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\Installer\Products")
        ]
        
        seen_names = set()  # Avoid duplicates
        
        for hive, reg_path in reg_paths:
            try:
                with winreg.OpenKey(hive, reg_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                software_info = self._extract_windows_software_info(subkey)
                                if software_info and software_info['name'] not in seen_names:
                                    seen_names.add(software_info['name'])
                                    software.append(software_info)
                        except Exception:
                            continue
            except Exception:
                continue
        
        # Also scan Program Files directories
        program_dirs = [
            os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
            os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs')
        ]
        
        for prog_dir in program_dirs:
            if prog_dir and os.path.exists(prog_dir):
                try:
                    for item in os.listdir(prog_dir):
                        item_path = os.path.join(prog_dir, item)
                        if os.path.isdir(item_path) and item not in seen_names:
                            seen_names.add(item)
                            software.append({
                                "name": item,
                                "version": "Unknown",
                                "publisher": "Unknown",
                                "install_date": "Unknown",
                                "size": self._get_dir_size(item_path),
                                "uninstall_string": f"rmdir /s /q \"{item_path}\"",
                                "install_location": item_path,
                                "type": "installed_software",
                                "platform": "Windows"
                            })
                except PermissionError:
                    continue
        
        return software
    
    def _scan_windows_store_apps(self) -> List[Dict]:
        """Scan Windows Store/UWP apps"""
        apps = []
        try:
            # Use PowerShell to get Windows Store apps
            ps_cmd = "Get-AppxPackage | Select-Object Name, Version, Publisher, InstallLocation | ConvertTo-Json"
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                app_data = json.loads(result.stdout)
                if isinstance(app_data, dict):
                    app_data = [app_data]
                
                for app in app_data:
                    apps.append({
                        "name": app.get('Name', 'Unknown'),
                        "version": app.get('Version', 'Unknown'),
                        "publisher": app.get('Publisher', 'Unknown'),
                        "install_date": "Unknown",
                        "size": 0,
                        "uninstall_string": f"Get-AppxPackage {app.get('Name')} | Remove-AppxPackage",
                        "install_location": app.get('InstallLocation', ''),
                        "type": "windows_store_app",
                        "platform": "Windows"
                    })
        except Exception as e:
            self.logger.error(f"Failed to scan Store apps: {e}")
        
        return apps
    
    def _extract_windows_software_info(self, key) -> Optional[Dict]:
        """Extract detailed software information from registry"""
        try:
            name = self._get_reg_value(key, "DisplayName")
            if not name:
                return None
            
            # Skip Windows updates and patches
            if name.startswith("Security Update") or name.startswith("Update for"):
                return None
            
            install_location = self._get_reg_value(key, "InstallLocation", "")
            
            return {
                "name": name,
                "version": self._get_reg_value(key, "DisplayVersion", "Unknown"),
                "publisher": self._get_reg_value(key, "Publisher", "Unknown"),
                "install_date": self._get_reg_value(key, "InstallDate", "Unknown"),
                "size": self._get_reg_value(key, "EstimatedSize", 0),
                "uninstall_string": self._get_reg_value(key, "UninstallString", ""),
                "install_location": install_location,
                "type": "installed_software",
                "platform": "Windows"
            }
        except Exception:
            return None
    
    def _get_reg_value(self, key, value_name, default=None):
        """Get registry value safely"""
        try:
            value, _ = winreg.QueryValueEx(key, value_name)
            return value
        except:
            return default
    
    def _scan_linux_software(self) -> List[Dict]:
        """Enhanced Linux software scanning - COMPREHENSIVE"""
        software = []
        
        # Try multiple package managers
        package_managers = [
            ("dpkg", ["dpkg-query", "-W", "-f='${Package}|${Version}|${Installed-Size}|${Status}\n'"]),
            ("rpm", ["rpm", "-qa", "--queryformat", "%{NAME}|%{VERSION}|%{SIZE}|installed\n"]),
            ("pacman", ["pacman", "-Q"]),
            ("snap", ["snap", "list"]),
            ("flatpak", ["flatpak", "list", "--app"]),
            ("appimage", self._scan_appimages),  # Custom function
            ("portage", ["equery", "list", "*"]),  # Gentoo
            ("zypper", ["zypper", "search", "-i"]),  # openSUSE
            ("yum", ["yum", "list", "installed"]),  # Older RHEL/CentOS
            ("dnf", ["dnf", "list", "installed"]),  # Fedora/newer RHEL
        ]
        
        for pm_name, cmd in package_managers:
            if isinstance(cmd, list):
                if shutil.which(cmd[0]):
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            software.extend(self._parse_package_output(pm_name, result.stdout))
                    except subprocess.TimeoutExpired:
                        self.logger.warning(f"Timeout scanning {pm_name}")
                    except Exception as e:
                        self.logger.error(f"Error scanning {pm_name}: {e}")
            else:
                # Custom function
                try:
                    software.extend(cmd())
                except Exception as e:
                    self.logger.error(f"Error in custom scanner {pm_name}: {e}")
        
        # Also scan common application directories
        app_dirs = [
            "/usr/bin",
            "/usr/local/bin",
            "/opt",
            "/usr/share/applications",
            os.path.expanduser("~/.local/bin"),
            os.path.expanduser("~/.local/share/applications"),
        ]
        
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for item in os.listdir(app_dir):
                        item_path = os.path.join(app_dir, item)
                        # Check if it's an executable or .desktop file
                        if (os.path.isfile(item_path) and 
                            (os.access(item_path, os.X_OK) or item.endswith('.desktop'))):
                            if not any(s['name'] == item for s in software):
                                software.append({
                                    "name": item,
                                    "version": "Unknown",
                                    "publisher": "System",
                                    "install_date": "Unknown",
                                    "size": os.path.getsize(item_path) // 1024 if os.path.isfile(item_path) else 0,
                                    "uninstall_string": f"rm -f '{item_path}'",
                                    "install_location": item_path,
                                    "type": "installed_software",
                                    "platform": "Linux"
                                })
                except PermissionError:
                    continue
        
        return software
    
    def _scan_appimages(self) -> List[Dict]:
        """Scan for AppImage files"""
        appimages = []
        search_dirs = [
            os.path.expanduser("~/Applications"),
            os.path.expanduser("~/bin"),
            "/opt",
            "/usr/local/bin",
        ]
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if file.endswith('.AppImage') or 'appimage' in file.lower():
                            file_path = os.path.join(root, file)
                            appimages.append({
                                "name": file,
                                "version": "Unknown",
                                "publisher": "AppImage",
                                "install_date": "Unknown",
                                "size": os.path.getsize(file_path) // 1024 // 1024,
                                "uninstall_string": f"rm -f '{file_path}'",
                                "install_location": file_path,
                                "type": "appimage",
                                "platform": "Linux"
                            })
        
        return appimages
    
    def _parse_package_output(self, pm_name: str, output: str) -> List[Dict]:
        """Parse package manager output"""
        packages = []
        
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            try:
                if pm_name == "dpkg":
                    # Parse dpkg output
                    line = line.strip("'")
                    parts = line.split('|')
                    if len(parts) >= 4 and 'installed' in parts[3]:
                        packages.append({
                            "name": parts[0],
                            "version": parts[1],
                            "publisher": "APT",
                            "install_date": "Unknown",
                            "size": int(parts[2]) if parts[2].isdigit() else 0,
                            "uninstall_string": f"sudo apt remove {parts[0]}",
                            "type": "installed_software",
                            "platform": "Linux"
                        })
                elif pm_name == "rpm":
                    # Parse RPM output
                    parts = line.split('|')
                    if len(parts) >= 3:
                        packages.append({
                            "name": parts[0],
                            "version": parts[1],
                            "publisher": "RPM",
                            "install_date": "Unknown",
                            "size": int(parts[2]) // 1024 if parts[2].isdigit() else 0,
                            "uninstall_string": f"sudo rpm -e {parts[0]}",
                            "type": "installed_software",
                            "platform": "Linux"
                        })
                elif pm_name == "snap":
                    # Parse snap output
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] != "Name":  # Skip header
                        packages.append({
                            "name": parts[0],
                            "version": parts[1] if len(parts) > 1 else "Unknown",
                            "publisher": "Snap",
                            "install_date": "Unknown",
                            "size": 0,
                            "uninstall_string": f"sudo snap remove {parts[0]}",
                            "type": "snap_package",
                            "platform": "Linux"
                        })
            except Exception:
                continue
        
        return packages
    
    def _scan_running_processes(self) -> List[Dict]:
        """Scan currently running processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time', 'exe']):
            try:
                pinfo = proc.info
                # Skip system processes on Windows
                if self.system == "Windows" and pinfo['name'] in ['System', 'Registry', 'smss.exe']:
                    continue
                
                exe_path = pinfo.get('exe', '')
                
                processes.append({
                    "name": f"[PROCESS] {pinfo['name']}",
                    "version": f"PID: {pinfo['pid']}",
                    "publisher": "Running Process",
                    "install_date": datetime.fromtimestamp(pinfo['create_time']).strftime('%Y-%m-%d'),
                    "size": pinfo['memory_info'].rss // 1024 // 1024,  # MB
                    "uninstall_string": f"taskkill /F /PID {pinfo['pid']}" if self.system == "Windows" else f"kill -9 {pinfo['pid']}",
                    "install_location": exe_path,
                    "type": "running_process",
                    "platform": self.system,
                    "pid": pinfo['pid']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
    def _scan_macos_software(self) -> List[Dict]:
        """Enhanced macOS software scanning - COMPREHENSIVE"""
        software = []
        
        # Scan Applications directories
        app_dirs = [
            "/Applications",
            os.path.expanduser("~/Applications"),
            "/System/Applications",
            "/System/Library/CoreServices",
            "/usr/local/Cellar",  # Homebrew Cask
        ]
        
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for item in os.listdir(app_dir):
                        if item.endswith(".app") or (app_dir.endswith("Cellar") and os.path.isdir(os.path.join(app_dir, item))):
                            app_path = os.path.join(app_dir, item)
                            try:
                                if item.endswith(".app"):
                                    info_plist = os.path.join(app_path, "Contents", "Info.plist")
                                    
                                    # Get version from Info.plist if possible
                                    version = "Unknown"
                                    publisher = "Unknown"
                                    if os.path.exists(info_plist):
                                        try:
                                            import plistlib
                                            with open(info_plist, 'rb') as f:
                                                plist = plistlib.load(f)
                                                version = plist.get('CFBundleShortVersionString', 
                                                                   plist.get('CFBundleVersion', 'Unknown'))
                                                publisher = plist.get('CFBundleIdentifier', 'Unknown')
                                        except:
                                            pass
                                    
                                    software.append({
                                        "name": item[:-4],  # Remove .app
                                        "version": version,
                                        "publisher": publisher,
                                        "install_date": "Unknown",
                                        "size": self._get_dir_size(app_path),
                                        "uninstall_string": f"sudo rm -rf '{app_path}'",
                                        "install_location": app_path,
                                        "type": "macos_app",
                                        "platform": "Darwin"
                                    })
                                elif app_dir.endswith("Cellar"):
                                    # Homebrew formula
                                    software.append({
                                        "name": item,
                                        "version": "Unknown",
                                        "publisher": "Homebrew",
                                        "install_date": "Unknown",
                                        "size": self._get_dir_size(app_path),
                                        "uninstall_string": f"brew uninstall {item}",
                                        "install_location": app_path,
                                        "type": "homebrew_formula",
                                        "platform": "Darwin"
                                    })
                            except Exception:
                                continue
                except PermissionError:
                    continue
        
        # Check Homebrew
        if shutil.which("brew"):
            try:
                # List all Homebrew packages
                result = subprocess.run(
                    ["brew", "list", "--versions"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                for line in result.stdout.splitlines():
                    parts = line.split()
                    if len(parts) >= 2:
                        software.append({
                            "name": parts[0],
                            "version": " ".join(parts[1:]),
                            "publisher": "Homebrew",
                            "install_date": "Unknown",
                            "size": 0,
                            "uninstall_string": f"brew uninstall {parts[0]}",
                            "type": "homebrew_package",
                            "platform": "Darwin"
                        })
                
                # Check Homebrew Cask
                result = subprocess.run(
                    ["brew", "list", "--cask", "--versions"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                for line in result.stdout.splitlines():
                    parts = line.split()
                    if len(parts) >= 2:
                        software.append({
                            "name": parts[0],
                            "version": " ".join(parts[1:]),
                            "publisher": "Homebrew Cask",
                            "install_date": "Unknown",
                            "size": 0,
                            "uninstall_string": f"brew uninstall --cask {parts[0]}",
                            "type": "homebrew_cask",
                            "platform": "Darwin"
                        })
            except Exception as e:
                self.logger.debug(f"Error scanning Homebrew: {e}")
        
        # Check MacPorts
        if shutil.which("port"):
            try:
                result = subprocess.run(
                    ["port", "installed"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                for line in result.stdout.splitlines():
                    if line.strip() and not line.startswith("The following"):
                        parts = line.split()
                        if len(parts) >= 2:
                            software.append({
                                "name": parts[0],
                                "version": parts[1] if len(parts) > 1 else "Unknown",
                                "publisher": "MacPorts",
                                "install_date": "Unknown",
                                "size": 0,
                                "uninstall_string": f"sudo port uninstall {parts[0]}",
                                "type": "macports_package",
                                "platform": "Darwin"
                            })
            except Exception:
                pass
        
        return software
    
    def _get_dir_size(self, path):
        """Calculate directory size"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_dir_size(entry.path)
        except (PermissionError, OSError):
            pass
        return total // 1024 // 1024  # Return in MB

class SoftwareRemover:
    """Enhanced software remover with aggressive permission handling"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
        self.dry_run = False
        self.permission_manager = PermissionManager(logger)
        
    def set_dry_run(self, enabled: bool):
        """Enable/disable dry run mode"""
        self.dry_run = enabled
        self.logger.info(f"Dry run mode: {'ENABLED' if enabled else 'DISABLED'}")
    
    def remove_software(self, software_info: Dict, force: bool = False) -> bool:
        """Remove software with enhanced permission handling"""
        self.logger.info(f"Starting removal of: {software_info['name']}")
        
        if self.dry_run:
            self.logger.info("DRY RUN: Would remove software")
            return True
        
        # Create system restore point (Windows)
        if self.system == "Windows" and software_info['type'] != 'running_process':
            self._create_restore_point(software_info['name'])
        
        # Stop related processes first
        self._stop_related_processes(software_info)
        
        # Handle different software types
        success = False
        
        if software_info['type'] == 'running_process':
            success = self._terminate_process(software_info)
        elif software_info['type'] == 'windows_store_app':
            success = self._remove_windows_store_app(software_info)
        else:
            # Try standard uninstall first
            success = self._uninstall_software(software_info)
            
            # If failed or force mode, use aggressive removal
            if not success or force:
                self.logger.warning("Standard uninstall failed, using force removal")
                success = self._force_remove_software(software_info)
        
        return success
    
    def _force_remove_software(self, software_info: Dict) -> bool:
        """Aggressively remove software"""
        self.logger.info("Starting force removal")
        
        # Get installation location
        install_location = software_info.get('install_location', '')
        
        if install_location and os.path.exists(install_location):
            # Take ownership first
            self.permission_manager.force_take_ownership(install_location)
            
            # Unlock any files in use
            self.permission_manager.unlock_file(install_location)
            
            # Remove directory
            try:
                if os.path.isdir(install_location):
                    # Use system commands for stubborn directories
                    if self.system == "Windows":
                        # Use rd command with force
                        subprocess.run(
                            f'rd /s /q "{install_location}"',
                            shell=True,
                            capture_output=True
                        )
                    else:
                        subprocess.run(
                            ['sudo', 'rm', '-rf', install_location],
                            capture_output=True
                        )
                    
                    # Verify removal
                    if not os.path.exists(install_location):
                        self.logger.info(f"Force removed: {install_location}")
                    else:
                        # Try even more aggressive approach
                        self._ultra_force_remove(install_location)
                
            except Exception as e:
                self.logger.error(f"Force removal failed: {e}")
                return False
        
        # Clean up registry and other traces
        self._cleanup_all_traces(software_info)
        
        return True
    
    def _ultra_force_remove(self, path: str):
        """Ultra aggressive removal for stubborn files/directories - ENHANCED"""
        self.logger.warning(f"Using ultra force removal on: {path}")
        
        if self.system == "Windows":
            # Method 1: Boot-time deletion scheduling
            try:
                import win32file
                win32file.MoveFileEx(
                    path,
                    None,
                    win32file.MOVEFILE_DELAY_UNTIL_REBOOT
                )
                self.logger.info("Scheduled for deletion on next reboot")
            except:
                pass
            
            # Method 2: Try using short path names
            try:
                short_path = win32api.GetShortPathName(path)
                os.system(f'del /f /s /q "{short_path}"')
                os.system(f'rd /s /q "{short_path}"')
            except:
                pass
            
            # Method 3: Use PowerShell with -Force -Recurse
            try:
                ps_cmd = f'Remove-Item -Path "{path}" -Force -Recurse -ErrorAction SilentlyContinue'
                subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    capture_output=True,
                    timeout=30
                )
            except:
                pass
            
            # Method 4: Use takeown + icacls + del
            try:
                subprocess.run(f'takeown /f "{path}" /r /d y', shell=True, capture_output=True)
                subprocess.run(f'icacls "{path}" /grant administrators:F /t /c /q', shell=True, capture_output=True)
                subprocess.run(f'rd /s /q "{path}"', shell=True, capture_output=True)
            except:
                pass
            
            # Method 5: Use robocopy mirror trick (creates empty dir, mirrors to target, deletes)
            try:
                temp_empty = tempfile.mkdtemp()
                subprocess.run(
                    f'robocopy "{temp_empty}" "{path}" /MIR /NFL /NDL /NJH /NJS',
                    shell=True,
                    capture_output=True
                )
                shutil.rmtree(temp_empty, ignore_errors=True)
            except:
                pass
        else:
            # Unix/Linux/MacOS ultra force methods
            # Method 1: chattr -R -i (remove immutable flag) then delete
            try:
                subprocess.run(['sudo', 'chattr', '-R', '-i', path], capture_output=True, timeout=10)
                subprocess.run(['sudo', 'rm', '-rf', path], capture_output=True)
            except:
                pass
            
            # Method 2: Use find with -delete
            try:
                subprocess.run(['sudo', 'find', path, '-delete'], capture_output=True, timeout=30)
            except:
                pass
            
            # Method 3: Use shred for files, then rm for dirs
            if os.path.isfile(path):
                try:
                    subprocess.run(['sudo', 'shred', '-f', '-u', '-z', path], capture_output=True, timeout=60)
                except:
                    subprocess.run(['sudo', 'rm', '-f', path], capture_output=True)
            else:
                # For directories, recursively shred all files then remove
                try:
                    for root, dirs, files in os.walk(path, topdown=False):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                subprocess.run(['sudo', 'shred', '-f', '-u', '-z', file_path], 
                                             capture_output=True, timeout=10)
                            except:
                                subprocess.run(['sudo', 'rm', '-f', file_path], capture_output=True)
                        for dir_name in dirs:
                            dir_path = os.path.join(root, dir_name)
                            subprocess.run(['sudo', 'rmdir', dir_path], capture_output=True)
                    subprocess.run(['sudo', 'rmdir', path], capture_output=True)
                except:
                    subprocess.run(['sudo', 'rm', '-rf', path], capture_output=True)
            
            # Method 4: Use lsof to kill processes, then remove
            try:
                result = subprocess.run(['lsof', path], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.splitlines()[1:]:
                        parts = line.split()
                        if len(parts) > 1:
                            pid = parts[1]
                            try:
                                subprocess.run(['sudo', 'kill', '-9', pid], capture_output=True)
                            except:
                                pass
                    time.sleep(0.5)
                    subprocess.run(['sudo', 'rm', '-rf', path], capture_output=True)
            except:
                pass
    
    def _remove_windows_store_app(self, software_info: Dict) -> bool:
        """Remove Windows Store/UWP apps"""
        try:
            app_name = software_info['name']
            
            # Use PowerShell to remove
            ps_cmd = f"Get-AppxPackage -Name '{app_name}' | Remove-AppxPackage"
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f"Store app removed: {app_name}")
                return True
            else:
                # Try with wildcard
                ps_cmd = f"Get-AppxPackage -Name '*{app_name}*' | Remove-AppxPackage"
                subprocess.run(["powershell", "-Command", ps_cmd])
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to remove Store app: {e}")
            return False
    
    def _create_restore_point(self, software_name: str):
        """Create Windows system restore point"""
        if self.system != "Windows":
            return
        
        try:
            # Enable system restore if needed
            subprocess.run(
                'powershell Enable-ComputerRestore -Drive "C:\\"',
                shell=True,
                capture_output=True
            )
            
            # Create restore point
            cmd = f'powershell Checkpoint-Computer -Description "Terminus - Before removing {software_name}" -RestorePointType "MODIFY_SETTINGS"'
            subprocess.run(cmd, shell=True, capture_output=True)
            self.logger.info("System restore point created")
        except Exception as e:
            self.logger.warning(f"Could not create restore point: {e}")
    
    def _stop_related_processes(self, software_info: Dict):
        """Stop all processes related to the software"""
        software_name = software_info['name'].lower()
        install_location = software_info.get('install_location', '').lower()
        
        terminated = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                pinfo = proc.info
                
                # Check if process is related
                related = False
                
                # Check process name
                if pinfo['name'] and software_name in pinfo['name'].lower():
                    related = True
                
                # Check executable path
                if pinfo['exe'] and install_location and install_location in pinfo['exe'].lower():
                    related = True
                
                # Check command line
                if pinfo['cmdline']:
                    cmdline = ' '.join(pinfo['cmdline']).lower()
                    if software_name in cmdline or (install_location and install_location in cmdline):
                        related = True
                
                if related and pinfo['pid'] not in terminated:
                    self.logger.info(f"Terminating related process: {pinfo['name']} (PID: {pinfo['pid']})")
                    try:
                        proc.terminate()
                        proc.wait(timeout=5)
                        terminated.append(pinfo['pid'])
                    except psutil.TimeoutExpired:
                        proc.kill()
                        terminated.append(pinfo['pid'])
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def _terminate_process(self, process_info: Dict) -> bool:
        """Terminate a running process"""
        try:
            pid = process_info.get('pid')
            if not pid:
                return False
            
            proc = psutil.Process(pid)
            
            # Try graceful termination first
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                # Force kill if needed
                proc.kill()
                proc.wait(timeout=5)
            
            self.logger.info(f"Process {process_info['name']} terminated")
            return True
            
        except psutil.NoSuchProcess:
            self.logger.info("Process already terminated")
            return True
        except Exception as e:
            self.logger.error(f"Failed to terminate process: {e}")
            
            # Try system commands
            if self.system == "Windows":
                subprocess.run(f"taskkill /F /PID {pid}", shell=True)
            else:
                subprocess.run(f"kill -9 {pid}", shell=True)
            
            return True
    
    def _uninstall_software(self, software_info: Dict) -> bool:
        """Run the software's uninstaller"""
        uninstall_string = software_info.get('uninstall_string', '')
        
        if not uninstall_string:
            self.logger.warning("No uninstall string found")
            return False
        
        try:
            self.logger.info(f"Running uninstaller: {uninstall_string}")
            
            # Add quiet/silent flags
            if self.system == "Windows":
                if "msiexec" in uninstall_string.lower():
                    if "/quiet" not in uninstall_string:
                        uninstall_string += " /quiet /norestart"
                elif ".exe" in uninstall_string.lower():
                    # Try common silent switches
                    for silent_switch in ["/S", "/SILENT", "/VERYSILENT", "-silent", "--uninstall"]:
                        if silent_switch not in uninstall_string:
                            test_cmd = f"{uninstall_string} {silent_switch}"
                            result = subprocess.run(test_cmd, shell=True, capture_output=True, timeout=60)
                            if result.returncode == 0:
                                uninstall_string = test_cmd
                                break
            
            # Execute uninstaller
            result = subprocess.run(
                uninstall_string,
                shell=True,
                capture_output=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.logger.info("Uninstaller completed successfully")
                return True
            else:
                self.logger.warning(f"Uninstaller returned code: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Uninstaller timed out")
            return False
        except Exception as e:
            self.logger.error(f"Uninstall failed: {e}")
            return False
    
    def _cleanup_all_traces(self, software_info: Dict):
        """Clean up all traces of software"""
        software_name = software_info['name']
        
        # Clean registry
        self._cleanup_registry(software_info)
        
        # Clean common directories
        self._cleanup_directories(software_info)
        
        # Clean scheduled tasks
        self._remove_scheduled_tasks(software_info)
        
        # Clean services
        self._remove_services(software_info)
    
    def _cleanup_registry(self, software_info: Dict):
        """Clean Windows registry entries"""
        if self.system != "Windows":
            return
        
        software_name = software_info['name'].lower()
        
        # All registry locations to check
        reg_locations = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE"),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services"),
            (winreg.HKEY_CLASSES_ROOT, r"Installer\Products"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData")
        ]
        
        for hive, path in reg_locations:
            try:
                self._clean_registry_path(hive, path, software_name)
            except Exception as e:
                self.logger.debug(f"Registry cleanup error: {e}")
    
    def _clean_registry_path(self, hive, path, software_name):
        """Recursively clean registry path"""
        try:
            with winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS) as key:
                # Get all subkeys
                subkeys = []
                i = 0
                while True:
                    try:
                        subkeys.append(winreg.EnumKey(key, i))
                        i += 1
                    except WindowsError:
                        break
                
                # Check each subkey
                for subkey_name in subkeys:
                    if software_name in subkey_name.lower():
                        try:
                            winreg.DeleteKey(key, subkey_name)
                            self.logger.info(f"Deleted registry key: {subkey_name}")
                        except:
                            # Try to delete recursively
                            self._delete_registry_tree(hive, f"{path}\\{subkey_name}")
                    else:
                        # Check inside subkey
                        try:
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    value = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if software_name in str(value).lower():
                                        winreg.DeleteKey(key, subkey_name)
                                        self.logger.info(f"Deleted registry key: {subkey_name}")
                                except:
                                    pass
                        except:
                            pass
        except Exception:
            pass
    
    def _delete_registry_tree(self, hive, key_path):
        """Delete registry key tree"""
        try:
            # Use reg command for recursive deletion
            hive_name = {
                winreg.HKEY_LOCAL_MACHINE: "HKLM",
                winreg.HKEY_CURRENT_USER: "HKCU",
                winreg.HKEY_CLASSES_ROOT: "HKCR"
            }.get(hive, "HKLM")
            
            subprocess.run(
                f'reg delete "{hive_name}\\{key_path}" /f',
                shell=True,
                capture_output=True
            )
        except:
            pass
    
    def _cleanup_directories(self, software_info: Dict):
        """Clean up remaining directories"""
        software_name = software_info['name'].lower().replace(' ', '')
        
        # Common installation directories
        if self.system == "Windows":
            search_dirs = [
                os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
                os.environ.get('LOCALAPPDATA', ''),
                os.environ.get('APPDATA', ''),
                os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData\\Local'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData\\Roaming'),
                'C:\\Windows\\Temp',
                os.environ.get('TEMP', '')
            ]
        else:
            search_dirs = [
                '/usr/local',
                '/opt',
                '/usr/share',
                '/etc',
                os.path.expanduser('~/.local'),
                os.path.expanduser('~/.config'),
                os.path.expanduser('~/.cache'),
                '/var/lib',
                '/var/cache'
            ]
        
        for base_dir in search_dirs:
            if not base_dir or not os.path.exists(base_dir):
                continue
            
            try:
                for item in os.listdir(base_dir):
                    if software_name in item.lower():
                        item_path = os.path.join(base_dir, item)
                        
                        # Take ownership and remove
                        self.permission_manager.force_take_ownership(item_path)
                        
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                        else:
                            os.remove(item_path)
                        
                        self.logger.info(f"Removed: {item_path}")
                        
            except (PermissionError, OSError) as e:
                self.logger.debug(f"Could not clean {base_dir}: {e}")
    
    def _remove_scheduled_tasks(self, software_info: Dict):
        """Remove scheduled tasks/cron jobs"""
        software_name = software_info['name'].lower()
        
        if self.system == "Windows":
            try:
                # List all scheduled tasks
                result = subprocess.run(
                    ["schtasks", "/query", "/fo", "csv"],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.splitlines()[1:]:
                    if software_name in line.lower():
                        # Extract task name
                        task_name = line.split(',')[0].strip('"')
                        subprocess.run(
                            ["schtasks", "/delete", "/tn", task_name, "/f"],
                            capture_output=True
                        )
                        self.logger.info(f"Removed scheduled task: {task_name}")
                        
            except Exception as e:
                self.logger.debug(f"Could not remove scheduled tasks: {e}")
        else:
            # Check crontab
            try:
                for cron_file in ["/etc/crontab", "/etc/cron.d/*", "/var/spool/cron/*"]:
                    # Remove entries containing software name
                    subprocess.run(
                        f"sudo sed -i '/{software_name}/d' {cron_file}",
                        shell=True,
                        capture_output=True
                    )
            except:
                pass
    
    def _remove_services(self, software_info: Dict):
        """Remove system services"""
        software_name = software_info['name'].lower()
        
        if self.system == "Windows":
            try:
                # List services
                result = subprocess.run(
                    ["sc", "query", "type=", "service"],
                    capture_output=True,
                    text=True
                )
                
                lines = result.stdout.splitlines()
                for i, line in enumerate(lines):
                    if "SERVICE_NAME:" in line and software_name in line.lower():
                        service_name = line.split("SERVICE_NAME:")[1].strip()
                        
                        # Stop and delete service
                        subprocess.run(["sc", "stop", service_name], capture_output=True)
                        subprocess.run(["sc", "delete", service_name], capture_output=True)
                        self.logger.info(f"Removed service: {service_name}")
                        
            except Exception as e:
                self.logger.debug(f"Could not remove services: {e}")
        else:
            # Linux systemd services
            try:
                result = subprocess.run(
                    ["systemctl", "list-units", "--type=service", "--all"],
                    capture_output=True,
                    text=True
                )
                
                for line in result.stdout.splitlines():
                    if software_name in line.lower():
                        parts = line.split()
                        if parts:
                            service_name = parts[0]
                            subprocess.run(["sudo", "systemctl", "stop", service_name])
                            subprocess.run(["sudo", "systemctl", "disable", service_name])
                            self.logger.info(f"Disabled service: {service_name}")
            except:
                pass

class FileDestroyer:
    """Secure file deletion with enhanced permission handling"""
    
    def __init__(self, logger):
        self.logger = logger
        self.permission_manager = PermissionManager(logger)
        
    def secure_delete(self, file_path: str, passes: int = SECURE_DELETE_PASSES) -> bool:
        """Securely delete a file with multiple overwrites - ENHANCED with more patterns"""
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
        
        try:
            # Take ownership first
            self.permission_manager.force_take_ownership(file_path)
            
            # Unlock file if in use
            self.permission_manager.unlock_file(file_path)
            
            file_size = os.path.getsize(file_path)
            
            # Enhanced wipe patterns (Gutmann + DoD 5220.22-M + Random)
            wipe_patterns = [
                b'\x00',  # Pass 1: All zeros
                b'\xFF',  # Pass 2: All ones
                b'\xAA',  # Pass 3: 10101010
                b'\x55',  # Pass 4: 01010101
                b'\x92',  # Pass 5: Random pattern 1
                b'\x49',  # Pass 6: Random pattern 2
                b'\x24',  # Pass 7: Random pattern 3
            ]
            
            with open(file_path, "ba+", buffering=0) as f:
                for pass_num in range(passes):
                    f.seek(0)
                    
                    # Select pattern based on pass number
                    if pass_num < len(wipe_patterns):
                        pattern = wipe_patterns[pass_num]
                    else:
                        # For additional passes, use random data
                        pattern = os.urandom(1)
                    
                    # Write pattern across entire file
                    chunk_size = 1024 * 1024  # 1MB chunks for efficiency
                    written = 0
                    while written < file_size:
                        chunk = pattern * min(chunk_size, file_size - written)
                        f.write(chunk)
                        written += len(chunk)
                    
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Final pass: write random data
                    if pass_num == passes - 1:
                        f.seek(0)
                        written = 0
                        while written < file_size:
                            chunk = os.urandom(min(chunk_size, file_size - written))
                            f.write(chunk)
                            written += len(chunk)
                        f.flush()
                        os.fsync(f.fileno())
                    
                    self.logger.info(f"Overwrite pass {pass_num + 1}/{passes} completed")
            
            # Rename file to random name before deletion (makes recovery harder)
            try:
                random_name = os.path.join(os.path.dirname(file_path), 
                                          f".tmp_{os.urandom(8).hex()}")
                os.rename(file_path, random_name)
                file_path = random_name
            except:
                pass
            
            # Final deletion
            os.remove(file_path)
            self.logger.info(f"File securely deleted: {file_path}")
            return True
            
        except PermissionError:
            # Try alternative deletion methods
            self.logger.warning("Permission denied, trying alternative methods")
            return self._force_delete_file(file_path)
        except Exception as e:
            self.logger.error(f"Secure delete failed: {e}")
            return False
    
    def _force_delete_file(self, file_path: str) -> bool:
        """Force delete a file using system commands"""
        try:
            if platform.system() == "Windows":
                # Try multiple methods
                methods = [
                    f'del /f /q "{file_path}"',
                    f'powershell Remove-Item -Path "{file_path}" -Force',
                    f'cmd /c "echo Y | cacls "{file_path}" /P everyone:F && del /f /q "{file_path}""'
                ]
                
                for method in methods:
                    result = subprocess.run(method, shell=True, capture_output=True)
                    if result.returncode == 0 and not os.path.exists(file_path):
                        self.logger.info("File force deleted")
                        return True
            else:
                subprocess.run(['sudo', 'rm', '-f', file_path])
                if not os.path.exists(file_path):
                    return True
                    
        except Exception as e:
            self.logger.error(f"Force delete failed: {e}")
            
        return False
    
    def secure_delete_directory(self, dir_path: str) -> bool:
        """Securely delete a directory and all contents"""
        if not os.path.exists(dir_path):
            self.logger.error(f"Directory not found: {dir_path}")
            return False
        
        try:
            # Take ownership of entire directory tree
            self.permission_manager.force_take_ownership(dir_path)
            
            # Walk through directory and securely delete files
            for root, dirs, files in os.walk(dir_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.secure_delete(file_path)
                
                # Remove empty directories
                for dir_name in dirs:
                    dir_full_path = os.path.join(root, dir_name)
                    try:
                        os.rmdir(dir_full_path)
                    except OSError:
                        # Force remove
                        if platform.system() == "Windows":
                            subprocess.run(f'rd /s /q "{dir_full_path}"', shell=True)
                        else:
                            subprocess.run(['sudo', 'rm', '-rf', dir_full_path])
            
            # Remove the main directory
            try:
                os.rmdir(dir_path)
            except:
                if platform.system() == "Windows":
                    subprocess.run(f'rd /s /q "{dir_path}"', shell=True)
                else:
                    subprocess.run(['sudo', 'rm', '-rf', dir_path])
                    
            self.logger.info(f"Directory securely deleted: {dir_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Directory deletion failed: {e}")
            return False
    
    def wipe_free_space(self, drive: str, size_mb: int = 100) -> bool:
        """Wipe free space on drive to prevent recovery"""
        self.logger.info(f"Wiping free space on {drive} ({size_mb}MB)...")
        
        try:
            # Create temporary file to fill free space
            temp_file = os.path.join(drive, f"terminus_wipe_{int(time.time())}.tmp")
            
            with open(temp_file, "wb") as f:
                written = 0
                chunk_size = 1024 * 1024  # 1MB chunks
                
                while written < size_mb * 1024 * 1024:
                    try:
                        f.write(os.urandom(chunk_size))
                        written += chunk_size
                    except OSError:
                        # Disk full
                        break
                
                f.flush()
                os.fsync(f.fileno())
            
            # Securely delete the temporary file
            self.secure_delete(temp_file)
            
            self.logger.info("Free space wipe completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Free space wipe failed: {e}")
            return False

class KeyboardHandler:
    """Proper keyboard input handling for navigation"""
    
    def __init__(self):
        self.system = platform.system()
        
    def get_key(self):
        """Get a single keypress - platform independent"""
        if self.system == "Windows":
            return self._get_key_windows()
        else:
            return self._get_key_unix()
    
    def _get_key_windows(self):
        """Windows keyboard input"""
        import msvcrt
        
        key = msvcrt.getch()
        
        # Handle special keys (arrows, etc)
        if key in [b'\x00', b'\xe0']:
            key = msvcrt.getch()
            key_map = {
                b'H': 'up',
                b'P': 'down',
                b'K': 'left',
                b'M': 'right',
                b'G': 'home',
                b'O': 'end',
                b'I': 'pageup',
                b'Q': 'pagedown'
            }
            return key_map.get(key, key.decode('utf-8', errors='ignore'))
        else:
            return key.decode('utf-8', errors='ignore')
    
    def _get_key_unix(self):
        """Unix/Linux keyboard input"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            
            # Check if input available
            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1)
                
                # Handle escape sequences (arrows, etc)
                if key == '\x1b':
                    key += sys.stdin.read(2)
                    key_map = {
                        '\x1b[A': 'up',
                        '\x1b[B': 'down',
                        '\x1b[C': 'right',
                        '\x1b[D': 'left',
                        '\x1b[H': 'home',
                        '\x1b[F': 'end',
                        '\x1b[5': 'pageup',
                        '\x1b[6': 'pagedown'
                    }
                    
                    # Read additional chars for pageup/pagedown
                    if key in ['\x1b[5', '\x1b[6']:
                        key += sys.stdin.read(1)
                        
                    return key_map.get(key, key)
                else:
                    return key
            else:
                return None
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

class TerminalUI:
    """Enhanced terminal UI with beautiful rendering and proper navigation"""
    
    def __init__(self, scanner, remover, destroyer, logger):
        self.scanner = scanner
        self.remover = remover
        self.destroyer = destroyer
        self.logger = logger
        self.software_list = []
        self.filtered_list = []
        self.selected_index = 0
        self.page_size = 15
        self.page = 0
        self.keyboard = KeyboardHandler()
        self.filter_type = "all"  # all, software, process
        self.ui = UIRenderer()
        
    def run(self):
        """Main UI loop"""
        while True:
            self.clear_screen()
            self.show_logo()
            choice = self.main_menu()
            
            if choice == '1':
                self.scan_software()
            elif choice == '2':
                self.remove_software_menu()
            elif choice == '3':
                self.file_destroyer_menu()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5':
                self.show_logs()
            elif choice == '6':
                print(f"\n{Fore.YELLOW}Thank you for using Terminus!{Style.RESET_ALL}")
                break
            else:
                print(f"\n{Fore.RED}Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_logo(self):
        """Display ASCII art logo"""
        print(Fore.CYAN + LOGO + Style.RESET_ALL)
    
    def main_menu(self) -> str:
        """Display beautiful main menu"""
        self.ui.print_header("MAIN MENU", 80)
        
        menu_items = [
            ("1", "Scan System Software", "🔍 Detect all installed software and processes"),
            ("2", "Remove Software", "🗑️  Remove any software with advanced methods"),
            ("3", "File Destroyer", "🔥 Securely delete files beyond recovery"),
            ("4", "Settings", "⚙️  Configure Terminus options"),
            ("5", "View Logs", "📋 View operation history"),
            ("6", "Exit", "👋 Exit Terminus")
        ]
        
        for num, title, desc in menu_items:
            print(f"  {Fore.CYAN}{Style.BRIGHT}{num}.{Style.RESET_ALL} {Fore.GREEN}{title:<25}{Style.RESET_ALL} {Fore.WHITE}{desc}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⚠️  WARNING:{Style.RESET_ALL} {Fore.YELLOW}Use with extreme caution! Always backup important data.{Style.RESET_ALL}")
        print(f"{Fore.RED}   This tool can permanently remove ANY software or file!{Style.RESET_ALL}\n")
        
        return input(f"{Fore.CYAN}{Style.BRIGHT}➜ Select option: {Style.RESET_ALL}")
    
    def scan_software(self):
        """Scan and display software with beautiful progress"""
        self.clear_screen()
        self.show_logo()
        self.ui.print_header("SYSTEM SCAN", 80)
        
        print(f"{Fore.CYAN}Scanning system for installed software...{Style.RESET_ALL}")
        print(f"{Fore.WHITE}This may take a few moments...{Style.RESET_ALL}\n")
        
        # Enhanced progress indicator with progress bar
        software_list = []
        scan_stages = [
            ("Scanning Windows Registry...", lambda: self.scanner._scan_windows_software() if platform.system() == "Windows" else []),
            ("Scanning Windows Store Apps...", lambda: self.scanner._scan_windows_store_apps() if platform.system() == "Windows" else []),
            ("Scanning Linux Packages...", lambda: self.scanner._scan_linux_software() if platform.system() == "Linux" else []),
            ("Scanning macOS Applications...", lambda: self.scanner._scan_macos_software() if platform.system() == "Darwin" else []),
            ("Scanning Running Processes...", lambda: self.scanner._scan_running_processes()),
        ]
        
        for stage_name, stage_func in scan_stages:
            print(f"{Fore.YELLOW}⏳ {stage_name}{Style.RESET_ALL}", end="", flush=True)
            try:
                result = stage_func()
                if isinstance(result, list):
                    software_list.extend(result)
                print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            except Exception as e:
                print(f" {Fore.RED}✗{Style.RESET_ALL} ({str(e)[:30]})")
        
        # Sort by type then name
        software_list.sort(key=lambda x: (x['type'], x['name'].lower()))
        self.software_list = software_list
        self.filtered_list = self.software_list.copy()
        
        # Show beautiful summary
        software_count = len([s for s in self.software_list if s['type'] != 'running_process'])
        process_count = len([s for s in self.software_list if s['type'] == 'running_process'])
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.GREEN}✓ Scan Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.CYAN}Installed Software:{Style.RESET_ALL} {Fore.YELLOW}{software_count:>6}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.CYAN}Running Processes:{Style.RESET_ALL}  {Fore.YELLOW}{process_count:>6}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.CYAN}Total Items:{Style.RESET_ALL}         {Fore.YELLOW}{len(self.software_list):>6}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def remove_software_menu(self):
        """Enhanced software removal interface with proper navigation"""
        if not self.software_list:
            print(f"\n{Fore.RED}No software scanned. Please scan first.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.show_logo()
            
            # Apply filter
            if self.filter_type == "software":
                self.filtered_list = [s for s in self.software_list if s['type'] != 'running_process']
            elif self.filter_type == "process":
                self.filtered_list = [s for s in self.software_list if s['type'] == 'running_process']
            else:
                self.filtered_list = self.software_list.copy()
            
            if not self.filtered_list:
                print(f"{Fore.YELLOW}No items match the current filter.{Style.RESET_ALL}")
                input("\nPress Enter to return...")
                self.filter_type = "all"
                continue
            
            # Ensure selected index is valid
            if self.selected_index >= len(self.filtered_list):
                self.selected_index = len(self.filtered_list) - 1
            
            print(f"{Fore.GREEN}=== Remove Software ==={Style.RESET_ALL}")
            print(f"Filter: {self.filter_type.upper()} | Total items: {len(self.filtered_list)}")
            
            # Calculate page
            self.page = self.selected_index // self.page_size
            start_idx = self.page * self.page_size
            end_idx = min(start_idx + self.page_size, len(self.filtered_list))
            
            print(f"Page {self.page + 1}/{(len(self.filtered_list) - 1) // self.page_size + 1}")
            print(f"\n{'#':<5} {'Name':<35} {'Version':<15} {'Size(MB)':<8} {'Type':<15}")
            print("-" * 80)
            
            # Display items
            for i in range(start_idx, end_idx):
                software = self.filtered_list[i]
                
                # Highlight selected item
                if i == self.selected_index:
                    print(f"{Back.WHITE}{Fore.BLACK}", end='')
                
                # Format name to fit
                name = software['name']
                if len(name) > 34:
                    name = name[:31] + "..."
                
                print(f"{i+1:<5} {name:<35} {software['version'][:14]:<15} "
                      f"{software['size']:<8} {software['type'][:14]:<15}")
                
                if i == self.selected_index:
                    print(Style.RESET_ALL, end='')
            
            # Show selected item details
            selected = self.filtered_list[self.selected_index]
            print(f"\n{Fore.CYAN}Selected:{Style.RESET_ALL} {selected['name']}")
            if selected.get('install_location'):
                print(f"{Fore.CYAN}Location:{Style.RESET_ALL} {selected['install_location']}")
            
            print(f"\n{Fore.YELLOW}Navigation:{Style.RESET_ALL}")
            print("↑/↓ = Navigate | PageUp/PageDown = Jump pages | Home/End = First/Last")
            print("Enter/R = Remove | F = Force Remove | A/S/P = Filter (All/Software/Process)")
            print("/ = Search | ESC/Q = Back to menu")
            
            # Get keyboard input
            key = self._get_key_with_timeout(0.1)
            
            if key:
                if key in ['q', 'Q', '\x1b']:  # ESC or Q
                    break
                elif key in ['up', 'k']:
                    self.selected_index = max(0, self.selected_index - 1)
                elif key in ['down', 'j']:
                    self.selected_index = min(len(self.filtered_list) - 1, self.selected_index + 1)
                elif key == 'pageup':
                    self.selected_index = max(0, self.selected_index - self.page_size)
                elif key == 'pagedown':
                    self.selected_index = min(len(self.filtered_list) - 1, self.selected_index + self.page_size)
                elif key == 'home':
                    self.selected_index = 0
                elif key == 'end':
                    self.selected_index = len(self.filtered_list) - 1
                elif key in ['\r', '\n', 'r', 'R']:  # Enter or R
                    self.confirm_and_remove(self.filtered_list[self.selected_index])
                    # Refresh list after removal
                    self.filtered_list = [s for s in self.filtered_list if s != self.filtered_list[self.selected_index]]
                    if self.selected_index >= len(self.filtered_list) and self.selected_index > 0:
                        self.selected_index -= 1
                elif key in ['f', 'F']:
                    self.confirm_and_remove(self.filtered_list[self.selected_index], force=True)
                elif key in ['a', 'A']:
                    self.filter_type = "all"
                elif key in ['s', 'S']:
                    self.filter_type = "software"
                elif key in ['p', 'P']:
                    self.filter_type = "process"
                elif key == '/':
                    self.search_software()
                elif key.isdigit():
                    # Jump to number
                    num = int(key)
                    if 1 <= num <= len(self.filtered_list):
                        self.selected_index = num - 1
    
    def _get_key_with_timeout(self, timeout):
        """Get keyboard input with timeout"""
        try:
            return self.keyboard.get_key()
        except:
            return None
    
    def search_software(self):
        """Search functionality"""
        print(f"\n{Fore.CYAN}Search:{Style.RESET_ALL} ", end='')
        search_term = input().lower()
        
        if search_term:
            # Find first match
            for i, software in enumerate(self.filtered_list):
                if search_term in software['name'].lower():
                    self.selected_index = i
                    break
    
    def confirm_and_remove(self, software: Dict, force: bool = False):
        """Confirm and remove software with beautiful UI"""
        self.clear_screen()
        self.show_logo()
        
        self.ui.print_header("CONFIRM REMOVAL", 80)
        
        # Display software info in a box
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}{Style.BRIGHT}Software Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Name:{Style.RESET_ALL}       {Fore.GREEN}{software['name']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Version:{Style.RESET_ALL}    {Fore.GREEN}{software['version']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Type:{Style.RESET_ALL}       {Fore.GREEN}{software['type']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Publisher:{Style.RESET_ALL}  {Fore.GREEN}{software.get('publisher', 'Unknown')}{Style.RESET_ALL}")
        
        if software.get('install_location'):
            loc = software['install_location']
            if len(loc) > 50:
                loc = loc[:47] + "..."
            print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Location:{Style.RESET_ALL}   {Fore.GREEN}{loc}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        if force:
            print(f"{Fore.RED}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.RED}⚠️  FORCE REMOVAL MODE - EXTREME DESTRUCTION ⚠️{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.YELLOW}This will:{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Take ownership of ALL files{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Kill ALL related processes{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Delete ALL files and directories{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Remove ALL registry entries{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Remove ALL services and scheduled tasks{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}    {Fore.WHITE}• Use multiple deletion methods{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.RED}{Style.BRIGHT}⚠️  WARNING: This action CANNOT be undone!{Style.RESET_ALL}\n")
        
        confirm = input(f"{Fore.CYAN}{Style.BRIGHT}Type 'YES' to confirm removal: {Style.RESET_ALL}")
        
        if confirm == 'YES':
            print(f"\n{Fore.YELLOW}Removing {software['name']}...{Style.RESET_ALL}\n")
            
            # Show progress
            with self.progress_spinner("Removing"):
                success = self.remover.remove_software(software, force=force)
            
            if success:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.GREEN}✓ Software removed successfully!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
                # Remove from lists
                if software in self.software_list:
                    self.software_list.remove(software)
                if software in self.filtered_list:
                    self.filtered_list.remove(software)
            else:
                print(f"\n{Fore.RED}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.RED}✗ Removal failed! Check logs for details.{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.YELLOW}Try using Force Remove (F) option.{Style.RESET_ALL}")
                print(f"{Fore.RED}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
            
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def file_destroyer_menu(self):
        """File destruction interface with beautiful UI"""
        while True:
            self.clear_screen()
            self.show_logo()
            self.ui.print_header("FILE DESTROYER", 80)
            
            menu_items = [
                ("1", "Secure Delete File", "🔥 Permanently delete a single file (7-pass wipe)"),
                ("2", "Secure Delete Directory", "🔥 Permanently delete entire directory tree"),
                ("3", "Wipe Free Space", "🧹 Overwrite free space to prevent recovery"),
                ("4", "Back to Main Menu", "← Return to main menu")
            ]
            
            for num, title, desc in menu_items:
                print(f"  {Fore.CYAN}{Style.BRIGHT}{num}.{Style.RESET_ALL} {Fore.GREEN}{title:<25}{Style.RESET_ALL} {Fore.WHITE}{desc}{Style.RESET_ALL}")
            
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  WARNING: File destruction is PERMANENT and IRREVERSIBLE!{Style.RESET_ALL}\n")
            
            choice = input(f"{Fore.CYAN}{Style.BRIGHT}➜ Select option: {Style.RESET_ALL}")
            
            if choice == '1':
                self.secure_delete_file()
            elif choice == '2':
                self.secure_delete_directory()
            elif choice == '3':
                self.wipe_free_space()
            elif choice == '4':
                break
    
    def secure_delete_file(self):
        """Secure file deletion with beautiful UI"""
        self.clear_screen()
        self.show_logo()
        self.ui.print_header("SECURE FILE DELETION", 80)
        
        print(f"{Fore.WHITE}Enter the full path to the file you want to permanently delete.{Style.RESET_ALL}")
        print(f"{Fore.RED}{Style.BRIGHT}WARNING: This will destroy the file beyond recovery!{Style.RESET_ALL}\n")
        
        file_path = input(f"{Fore.CYAN}File path: {Style.RESET_ALL}").strip().strip('"')
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / 1024 / 1024
            
            print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}{Style.BRIGHT}File Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Path:{Style.RESET_ALL}  {Fore.GREEN}{file_path[:60]}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Size:{Style.RESET_ALL}  {Fore.GREEN}{file_size_mb:.2f} MB ({file_size:,} bytes){Style.RESET_ALL}")
            print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Wipes:{Style.RESET_ALL} {Fore.GREEN}{SECURE_DELETE_PASSES} passes (DoD 5220.22-M + Random){Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
            
            print(f"{Fore.RED}{Style.BRIGHT}⚠️  This will PERMANENTLY destroy the file!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The file will be overwritten {SECURE_DELETE_PASSES} times before deletion.{Style.RESET_ALL}\n")
            
            confirm = input(f"{Fore.CYAN}{Style.BRIGHT}Type 'DELETE' to confirm: {Style.RESET_ALL}")
            
            if confirm == 'DELETE':
                print(f"\n{Fore.YELLOW}Securely deleting file...{Style.RESET_ALL}\n")
                
                # Show progress
                start_time = time.time()
                success = self.destroyer.secure_delete(file_path)
                elapsed = time.time() - start_time
                
                if success:
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.GREEN}✓ File securely deleted!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.WHITE}Time taken: {elapsed:.2f} seconds{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
                else:
                    print(f"\n{Fore.RED}{Style.BRIGHT}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
                    print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.RED}✗ Deletion failed! Check permissions.{Style.RESET_ALL}")
                    print(f"{Fore.RED}{Style.BRIGHT}║{Style.RESET_ALL}  {Fore.YELLOW}Try running as Administrator/Root{Style.RESET_ALL}")
                    print(f"{Fore.RED}{Style.BRIGHT}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.RED}✗ File not found or is a directory!{Style.RESET_ALL}\n")
        
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def secure_delete_directory(self):
        """Secure directory deletion"""
        self.clear_screen()
        print(f"{Fore.YELLOW}=== Secure Directory Deletion ==={Style.RESET_ALL}\n")
        print("Enter the full path to the directory you want to permanently delete.")
        print(f"{Fore.RED}WARNING: This will destroy ALL files in the directory!{Style.RESET_ALL}\n")
        
        dir_path = input("Directory path: ").strip().strip('"')
        
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            # Count files
            file_count = sum(len(files) for _, _, files in os.walk(dir_path))
            dir_size = self.scanner._get_dir_size(dir_path)
            
            print(f"\nDirectory: {dir_path}")
            print(f"Files: {file_count}")
            print(f"Total size: {dir_size} MB")
            
            print(f"\n{Fore.RED}⚠️  This will permanently destroy the directory and ALL contents!{Style.RESET_ALL}")
            confirm = input(f"\n{Fore.CYAN}Type 'DELETE ALL' to confirm: {Style.RESET_ALL}")
            
            if confirm == 'DELETE ALL':
                print(f"\n{Fore.YELLOW}Securely deleting directory...{Style.RESET_ALL}")
                if self.destroyer.secure_delete_directory(dir_path):
                    print(f"\n{Fore.GREEN}✓ Directory securely deleted!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}✗ Deletion failed! Check permissions.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Directory not found!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def wipe_free_space(self):
        """Wipe drive free space"""
        self.clear_screen()
        print(f"{Fore.YELLOW}=== Wipe Free Space ==={Style.RESET_ALL}\n")
        print("This will overwrite free space to prevent recovery of deleted files.\n")
        
        if platform.system() == "Windows":
            print("Enter drive letter (e.g., C: or C:\\)")
            drive = input("Drive: ").strip()
            if not drive.endswith(':') and not drive.endswith(':\\'):
                drive += ':\\'
        else:
            print("Enter mount point (e.g., / or /home)")
            drive = input("Mount point: ").strip()
        
        size_mb = input("Size to wipe in MB (default 100): ").strip()
        size_mb = int(size_mb) if size_mb.isdigit() else 100
        
        print(f"\n{Fore.YELLOW}This will temporarily create a {size_mb}MB file to overwrite free space.{Style.RESET_ALL}")
        confirm = input(f"\n{Fore.CYAN}Continue? (y/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 'y':
            print(f"\n{Fore.YELLOW}Wiping free space...{Style.RESET_ALL}")
            if self.destroyer.wipe_free_space(drive, size_mb):
                print(f"\n{Fore.GREEN}✓ Free space wiped!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}✗ Wipe failed!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Settings menu with beautiful UI"""
        while True:
            self.clear_screen()
            self.show_logo()
            self.ui.print_header("SETTINGS", 80)
            
            menu_items = [
                ("1", f"Dry Run Mode: {Fore.YELLOW}{'ON' if self.remover.dry_run else 'OFF'}{Style.RESET_ALL}", "Test mode - no actual deletions"),
                ("2", f"Log Level: {Fore.YELLOW}{logging.getLevelName(logging.getLogger().level)}{Style.RESET_ALL}", "Set logging verbosity"),
                ("3", f"Page Size: {Fore.YELLOW}{self.page_size} items{Style.RESET_ALL}", "Items per page in lists"),
                ("4", "Clear Logs", "Delete all log files"),
                ("5", "System Info", "Display system information"),
                ("6", "Back to Main Menu", "← Return to main menu")
            ]
            
            for num, title, desc in menu_items:
                print(f"  {Fore.CYAN}{Style.BRIGHT}{num}.{Style.RESET_ALL} {title:<40} {Fore.WHITE}{desc}{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.CYAN}{Style.BRIGHT}➜ Select option: {Style.RESET_ALL}")
            
            if choice == '1':
                self.remover.set_dry_run(not self.remover.dry_run)
                status = "ENABLED" if self.remover.dry_run else "DISABLED"
                print(f"\n{Fore.GREEN}Dry Run Mode {status}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == '2':
                self.change_log_level()
            elif choice == '3':
                self.change_page_size()
            elif choice == '4':
                self.clear_logs()
            elif choice == '5':
                self.show_system_info()
            elif choice == '6':
                break
    
    def change_page_size(self):
        """Change items per page"""
        print("\nEnter new page size (10-50): ", end='')
        try:
            size = int(input())
            if 10 <= size <= 50:
                self.page_size = size
                print(f"{Fore.GREEN}Page size changed to {size}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid size. Must be between 10-50.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
        
        time.sleep(1)
    
    def show_system_info(self):
        """Display beautiful system information"""
        self.clear_screen()
        self.show_logo()
        self.ui.print_header("SYSTEM INFORMATION", 80)
        
        # Get system info
        os_name = platform.system()
        os_release = platform.release()
        arch = platform.machine()
        processor = platform.processor()
        python_ver = sys.version.split()[0]
        
        # Privileges
        if os_name == "Windows":
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            privileges = "Administrator" if is_admin else "Standard User"
        else:
            privileges = "Root" if os.geteuid() == 0 else "Standard User"
        
        # Memory info
        mem = psutil.virtual_memory()
        mem_total = mem.total // (1024**3)
        mem_available = mem.available // (1024**3)
        mem_percent = mem.percent
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}{Style.BRIGHT}Operating System:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}OS:{Style.RESET_ALL}         {Fore.GREEN}{os_name} {os_release}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Architecture:{Style.RESET_ALL} {Fore.GREEN}{arch}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Processor:{Style.RESET_ALL}   {Fore.GREEN}{processor[:50]}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Python:{Style.RESET_ALL}     {Fore.GREEN}{python_ver}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Privileges:{Style.RESET_ALL} {Fore.GREEN}{privileges}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}{Style.BRIGHT}Memory:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Total:{Style.RESET_ALL}      {Fore.GREEN}{mem_total} GB{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Available:{Style.RESET_ALL} {Fore.GREEN}{mem_available} GB ({100-mem_percent}%){Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}Used:{Style.RESET_ALL}      {Fore.GREEN}{mem_percent}%{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.YELLOW}{Style.BRIGHT}Disk Space:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_gb = usage.total // (1024**3)
                free_gb = usage.free // (1024**3)
                used_percent = (usage.used / usage.total) * 100
                print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}{partition.mountpoint:<15}{Style.RESET_ALL} {Fore.GREEN}{free_gb:>6} GB free / {total_gb:>6} GB total ({used_percent:.1f}% used){Style.RESET_ALL}")
            except:
                pass
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def change_log_level(self):
        """Change logging level"""
        print("\n1. DEBUG (Most verbose)")
        print("2. INFO (Default)")
        print("3. WARNING")
        print("4. ERROR (Least verbose)")
        
        choice = input(f"\n{Fore.CYAN}Select level: {Style.RESET_ALL}")
        
        levels = {
            '1': logging.DEBUG,
            '2': logging.INFO,
            '3': logging.WARNING,
            '4': logging.ERROR
        }
        
        if choice in levels:
            logging.getLogger().setLevel(levels[choice])
            print(f"\n{Fore.GREEN}Log level changed!{Style.RESET_ALL}")
            time.sleep(1)
    
    def clear_logs(self):
        """Clear log files"""
        confirm = input(f"\n{Fore.CYAN}Clear all logs? (y/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 'y':
            try:
                for log_file in LOG_DIR.glob("*.log"):
                    log_file.unlink()
                print(f"\n{Fore.GREEN}Logs cleared!{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}Error clearing logs: {e}{Style.RESET_ALL}")
            
            time.sleep(1)
    
    def show_logs(self):
        """Display recent log entries"""
        self.clear_screen()
        print(f"{Fore.GREEN}=== Recent Logs ==={Style.RESET_ALL}\n")
        
        try:
            # Get most recent log file
            log_files = sorted(LOG_DIR.glob("*.log"), key=os.path.getmtime, reverse=True)
            
            if log_files:
                with open(log_files[0], 'r') as f:
                    lines = f.readlines()
                    # Show last 30 lines
                    for line in lines[-30:]:
                        if "ERROR" in line:
                            print(Fore.RED + line.strip() + Style.RESET_ALL)
                        elif "WARNING" in line:
                            print(Fore.YELLOW + line.strip() + Style.RESET_ALL)
                        elif "INFO" in line:
                            print(Fore.GREEN + line.strip() + Style.RESET_ALL)
                        else:
                            print(line.strip())
            else:
                print("No logs found.")
        except Exception as e:
            print(f"Error reading logs: {e}")
        
        input("\nPress Enter to continue...")
    
    def progress_spinner(self, message: str):
        """Context manager for progress spinner"""
        class Spinner:
            def __init__(self, message):
                self.message = message
                self.running = False
                self.thread = None
            
            def __enter__(self):
                self.running = True
                self.thread = threading.Thread(target=self._spin)
                self.thread.start()
                return self
            
            def __exit__(self, *args):
                self.running = False
                if self.thread:
                    self.thread.join()
                print('\r' + ' ' * (len(self.message) + 10) + '\r', end='')
            
            def _spin(self):
                spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
                i = 0
                while self.running:
                    print(f'\r{self.message} {spinners[i % len(spinners)]}', end='', flush=True)
                    i += 1
                    time.sleep(0.1)
        
        return Spinner(message)

def check_admin():
    """Check if running with admin/root privileges"""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def elevate_privileges():
    """Attempt to elevate privileges if not admin"""
    if check_admin():
        return True
    
    if platform.system() == "Windows":
        print(f"{Fore.YELLOW}Requesting administrator privileges...{Style.RESET_ALL}")
        try:
            # Re-run the script with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                1
            )
            sys.exit(0)
        except:
            print(f"{Fore.RED}Failed to elevate privileges{Style.RESET_ALL}")
            return False
    else:
        print(f"{Fore.YELLOW}Please run with sudo for full functionality{Style.RESET_ALL}")
        return False

def main():
    """Main entry point"""
    # Initialize components
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    logger = Logger()
    
    logger.info(f"Starting {APP_NAME} v{VERSION}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Architecture: {platform.machine()}")
    logger.info(f"Admin privileges: {'Yes' if check_admin() else 'No'}")
    logger.info(f"Python version: {sys.version.split()[0]}")
    
    # Check for admin privileges
    if not check_admin():
        print(f"\n{Fore.YELLOW}⚠️  WARNING: Not running with administrator privileges!{Style.RESET_ALL}")
        print("\nTerminus requires administrator/root privileges for:")
        print("  • Removing system software")
        print("  • Deleting protected files")
        print("  • Modifying system settings")
        print("\nSome features will not work without proper privileges.")
        
        if platform.system() == "Windows":
            response = input(f"\n{Fore.CYAN}Would you like to restart with admin privileges? (y/n): {Style.RESET_ALL}")
            if response.lower() == 'y':
                elevate_privileges()
        else:
            print(f"\n{Fore.CYAN}Please run with: sudo python3 {sys.argv[0]}{Style.RESET_ALL}")
        
        response = input(f"\n{Fore.CYAN}Continue with limited privileges? (y/n): {Style.RESET_ALL}")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Beautiful safety warning
    ui_renderer = UIRenderer()
    print(f"\n{Fore.RED}{Style.BRIGHT}{'═'*80}{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}{'⚠️  IMPORTANT SAFETY WARNING ⚠️'.center(80)}{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}{'═'*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}{Style.BRIGHT}Terminus {VERSION} is an ULTRA-POWERFUL tool that can:{Style.RESET_ALL}\n")
    print(f"  {Fore.RED}•{Style.RESET_ALL} Remove {Fore.RED}{Style.BRIGHT}ANY{Style.RESET_ALL} software including system components")
    print(f"  {Fore.RED}•{Style.RESET_ALL} Delete {Fore.RED}{Style.BRIGHT}ANY{Style.RESET_ALL} file regardless of permissions")
    print(f"  {Fore.RED}•{Style.RESET_ALL} Modify critical system settings and registry")
    print(f"  {Fore.RED}•{Style.RESET_ALL} Use multiple aggressive deletion methods")
    print(f"  {Fore.RED}•{Style.RESET_ALL} Potentially damage your operating system\n")
    
    print(f"{Fore.MAGENTA}{Style.BRIGHT}⚡ This version has ENHANCED capabilities:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} 7-pass secure file deletion (DoD 5220.22-M)")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Ultra-aggressive permission bypassing")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Multiple deletion methods per file")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Comprehensive software detection")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Cross-platform support (Windows/Linux/macOS)\n")
    
    print(f"{Fore.RED}{Style.BRIGHT}⚡ Use ONLY if you understand the risks!{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}⚡ ALWAYS backup important data first!{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}⚡ Test in a virtual machine first!{Style.RESET_ALL}\n")
    
    print(f"{Fore.RED}{Style.BRIGHT}{'═'*80}{Style.RESET_ALL}\n")
    
    confirm = input(f"{Fore.CYAN}{Style.BRIGHT}Type 'I UNDERSTAND THE RISKS' to continue: {Style.RESET_ALL}")
    
    if confirm != "I UNDERSTAND THE RISKS":
        print(f"\n{Fore.YELLOW}Exiting for safety. Please read the warnings carefully.{Style.RESET_ALL}")
        sys.exit(0)
    
    # Initialize components
    scanner = SystemScanner(logger)
    remover = SoftwareRemover(logger)
    destroyer = FileDestroyer(logger)
    
    # Create and run UI
    ui = TerminalUI(scanner, remover, destroyer, logger)
    
    try:
        ui.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"\n{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        print("Check logs for details.")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("Terminus shutting down")

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 10):
        print(f"{Fore.RED}Error: Python 3.10 or higher required{Style.RESET_ALL}")
        sys.exit(1)
    
    main()
