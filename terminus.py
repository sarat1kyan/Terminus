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
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import threading
import queue

# Third-party imports (install with pip)
try:
    import psutil
    import curses
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
except ImportError as e:
    print(f"Missing required module: {e}")
    print("Please install: pip install psutil colorama windows-curses")
    sys.exit(1)

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import winreg
        import win32api
        import win32security
        import win32con
        import ctypes
        from ctypes import wintypes
    except ImportError:
        print("Windows modules not found. Install: pip install pywin32")
        sys.exit(1)

# Constants
APP_NAME = "Terminus"
VERSION = "1.0.0"
LOG_DIR = Path.home() / ".terminus" / "logs"
CONFIG_DIR = Path.home() / ".terminus"
SECURE_DELETE_PASSES = 3  # DoD 5220.22-M standard

# ASCII Art Logo
LOGO = """

╔═══════════════════════════┤ Version v4.0 ├═════════════════════════════╗
║                                                                        ║
║  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██╗   ██╗███████╗    ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██║   ██║██╔════╝    ║
║     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║███████╗    ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║╚════██║    ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████║    ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ║
║                       Ultimate System Cleaner                          ║
╚════════════════════════════════════════════════════════════════════════╝

"""

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

class SystemScanner:
    """Scans system for installed software and processes"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
        
    def scan_installed_software(self) -> List[Dict]:
        """Scan for all installed software"""
        self.logger.info("Starting system software scan...")
        software_list = []
        
        if self.system == "Windows":
            software_list.extend(self._scan_windows_software())
        elif self.system == "Linux":
            software_list.extend(self._scan_linux_software())
        elif self.system == "Darwin":  # macOS
            software_list.extend(self._scan_macos_software())
        
        # Add running processes
        software_list.extend(self._scan_running_processes())
        
        self.logger.info(f"Found {len(software_list)} software items")
        return software_list
    
    def _scan_windows_software(self) -> List[Dict]:
        """Scan Windows registry for installed software"""
        software = []
        
        # Registry paths for installed software
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                software_info = self._extract_windows_software_info(subkey)
                                if software_info:
                                    software.append(software_info)
                        except Exception:
                            continue
            except Exception:
                continue
        
        return software
    
    def _extract_windows_software_info(self, key) -> Optional[Dict]:
        """Extract software information from Windows registry key"""
        try:
            name = self._get_reg_value(key, "DisplayName")
            if not name:
                return None
            
            return {
                "name": name,
                "version": self._get_reg_value(key, "DisplayVersion", "Unknown"),
                "publisher": self._get_reg_value(key, "Publisher", "Unknown"),
                "install_date": self._get_reg_value(key, "InstallDate", "Unknown"),
                "size": self._get_reg_value(key, "EstimatedSize", 0),
                "uninstall_string": self._get_reg_value(key, "UninstallString", ""),
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
        """Scan Linux system for installed packages"""
        software = []
        
        # Check for different package managers
        if shutil.which("dpkg"):
            software.extend(self._scan_dpkg_packages())
        if shutil.which("rpm"):
            software.extend(self._scan_rpm_packages())
        if shutil.which("pacman"):
            software.extend(self._scan_pacman_packages())
        
        return software
    
    def _scan_dpkg_packages(self) -> List[Dict]:
        """Scan Debian/Ubuntu packages"""
        packages = []
        try:
            result = subprocess.run(["dpkg", "-l"], capture_output=True, text=True)
            for line in result.stdout.splitlines()[5:]:  # Skip header
                if line.startswith("ii"):
                    parts = line.split()
                    if len(parts) >= 3:
                        packages.append({
                            "name": parts[1],
                            "version": parts[2],
                            "publisher": "APT",
                            "install_date": "Unknown",
                            "size": 0,
                            "uninstall_string": f"apt remove {parts[1]}",
                            "type": "installed_software",
                            "platform": "Linux"
                        })
        except Exception as e:
            self.logger.error(f"Error scanning dpkg packages: {e}")
        
        return packages
    
    def _scan_rpm_packages(self) -> List[Dict]:
        """Scan RPM-based system packages"""
        packages = []
        try:
            result = subprocess.run(["rpm", "-qa", "--queryformat", "%{NAME}|%{VERSION}|%{SIZE}\n"], 
                                  capture_output=True, text=True)
            for line in result.stdout.splitlines():
                parts = line.split("|")
                if len(parts) == 3:
                    packages.append({
                        "name": parts[0],
                        "version": parts[1],
                        "publisher": "RPM",
                        "install_date": "Unknown",
                        "size": int(parts[2]) if parts[2].isdigit() else 0,
                        "uninstall_string": f"rpm -e {parts[0]}",
                        "type": "installed_software",
                        "platform": "Linux"
                    })
        except Exception as e:
            self.logger.error(f"Error scanning RPM packages: {e}")
        
        return packages
    
    def _scan_pacman_packages(self) -> List[Dict]:
        """Scan Arch Linux packages"""
        packages = []
        try:
            result = subprocess.run(["pacman", "-Q"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({
                        "name": parts[0],
                        "version": parts[1],
                        "publisher": "Pacman",
                        "install_date": "Unknown",
                        "size": 0,
                        "uninstall_string": f"pacman -R {parts[0]}",
                        "type": "installed_software",
                        "platform": "Linux"
                    })
        except Exception as e:
            self.logger.error(f"Error scanning Pacman packages: {e}")
        
        return packages
    
    def _scan_macos_software(self) -> List[Dict]:
        """Scan macOS applications"""
        software = []
        
        # Scan Applications folder
        app_dirs = ["/Applications", os.path.expanduser("~/Applications")]
        
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                for item in os.listdir(app_dir):
                    if item.endswith(".app"):
                        app_path = os.path.join(app_dir, item)
                        try:
                            # Get app info from Info.plist
                            info_plist = os.path.join(app_path, "Contents", "Info.plist")
                            if os.path.exists(info_plist):
                                # Simple parsing - in production, use plistlib
                                software.append({
                                    "name": item[:-4],  # Remove .app extension
                                    "version": "Unknown",
                                    "publisher": "Unknown",
                                    "install_date": "Unknown",
                                    "size": self._get_dir_size(app_path),
                                    "uninstall_string": f"rm -rf '{app_path}'",
                                    "type": "installed_software",
                                    "platform": "Darwin"
                                })
                        except Exception:
                            continue
        
        # Also check Homebrew packages if available
        if shutil.which("brew"):
            try:
                result = subprocess.run(["brew", "list", "--versions"], 
                                      capture_output=True, text=True)
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
                            "type": "installed_software",
                            "platform": "Darwin"
                        })
            except Exception:
                pass
        
        return software
    
    def _scan_running_processes(self) -> List[Dict]:
        """Scan currently running processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time']):
            try:
                pinfo = proc.info
                processes.append({
                    "name": pinfo['name'],
                    "version": f"PID: {pinfo['pid']}",
                    "publisher": "System Process",
                    "install_date": datetime.fromtimestamp(pinfo['create_time']).strftime('%Y-%m-%d'),
                    "size": pinfo['memory_info'].rss // 1024 // 1024,  # MB
                    "uninstall_string": f"kill -9 {pinfo['pid']}",
                    "type": "running_process",
                    "platform": self.system,
                    "pid": pinfo['pid']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
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
    """Handles advanced software removal"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
        self.dry_run = False
        
    def set_dry_run(self, enabled: bool):
        """Enable/disable dry run mode"""
        self.dry_run = enabled
        self.logger.info(f"Dry run mode: {'ENABLED' if enabled else 'DISABLED'}")
    
    def remove_software(self, software_info: Dict, force: bool = False) -> bool:
        """Remove software with advanced techniques"""
        self.logger.info(f"Starting removal of: {software_info['name']}")
        
        if self.dry_run:
            self.logger.info("DRY RUN: Would remove software")
            return True
        
        # Create system restore point (Windows)
        if self.system == "Windows" and not software_info['type'] == 'running_process':
            self._create_restore_point(software_info['name'])
        
        # Stop related processes
        self._stop_related_processes(software_info)
        
        # Perform removal based on type
        if software_info['type'] == 'running_process':
            return self._terminate_process(software_info)
        else:
            success = self._uninstall_software(software_info)
            
            if success or force:
                # Clean up remaining files
                self._cleanup_files(software_info)
                
                # Clean registry/config
                self._cleanup_registry(software_info)
                
                # Remove scheduled tasks
                self._remove_scheduled_tasks(software_info)
        
        self.logger.info(f"Removal of {software_info['name']} completed")
        return True
    
    def _create_restore_point(self, software_name: str):
        """Create Windows system restore point"""
        if self.system != "Windows":
            return
        
        try:
            # Use WMI to create restore point
            subprocess.run([
                "wmic.exe", "/Namespace:\\\\root\\default", 
                "Path", "SystemRestore", "Call", 
                f"CreateRestorePoint", f"\"Terminus - Before removing {software_name}\"", 
                "100", "7"
            ], capture_output=True)
            self.logger.info("System restore point created")
        except Exception as e:
            self.logger.warning(f"Could not create restore point: {e}")
    
    def _stop_related_processes(self, software_info: Dict):
        """Stop processes related to the software"""
        software_name = software_info['name'].lower()
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pinfo = proc.info
                if (pinfo['name'] and software_name in pinfo['name'].lower()) or \
                   (pinfo['exe'] and software_name in pinfo['exe'].lower()):
                    self.logger.info(f"Terminating related process: {pinfo['name']} (PID: {pinfo['pid']})")
                    proc.terminate()
                    proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
    
    def _terminate_process(self, process_info: Dict) -> bool:
        """Terminate a running process"""
        try:
            pid = process_info.get('pid')
            if pid:
                proc = psutil.Process(pid)
                proc.terminate()
                proc.wait(timeout=5)
                self.logger.info(f"Process {process_info['name']} terminated")
                return True
        except psutil.NoSuchProcess:
            self.logger.info("Process already terminated")
            return True
        except Exception as e:
            self.logger.error(f"Failed to terminate process: {e}")
            return False
    
    def _uninstall_software(self, software_info: Dict) -> bool:
        """Run the software's uninstaller"""
        uninstall_string = software_info.get('uninstall_string', '')
        
        if not uninstall_string:
            self.logger.warning("No uninstall string found")
            return False
        
        try:
            # Execute uninstaller
            if self.system == "Windows":
                # Handle msiexec commands
                if "msiexec" in uninstall_string.lower():
                    uninstall_string += " /quiet /norestart"
                
                result = subprocess.run(uninstall_string, shell=True, capture_output=True)
            else:
                # Linux/macOS - may need sudo
                if os.geteuid() != 0:
                    self.logger.warning("Root privileges may be required")
                
                result = subprocess.run(uninstall_string.split(), capture_output=True)
            
            if result.returncode == 0:
                self.logger.info("Uninstaller completed successfully")
                return True
            else:
                self.logger.warning(f"Uninstaller returned code: {result.returncode}")
                return False
                
        except Exception as e:
            self.logger.error(f"Uninstall failed: {e}")
            return False
    
    def _cleanup_files(self, software_info: Dict):
        """Clean up remaining files and directories"""
        # Common installation directories to check
        if self.system == "Windows":
            search_dirs = [
                os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
                os.environ.get('LOCALAPPDATA', ''),
                os.environ.get('APPDATA', ''),
                os.environ.get('PROGRAMDATA', 'C:\\ProgramData')
            ]
        else:
            search_dirs = [
                '/usr/local',
                '/opt',
                os.path.expanduser('~/.local'),
                os.path.expanduser('~/.config'),
                '/etc'
            ]
        
        software_name = software_info['name'].lower().replace(' ', '')
        
        for base_dir in search_dirs:
            if not base_dir or not os.path.exists(base_dir):
                continue
            
            try:
                for item in os.listdir(base_dir):
                    if software_name in item.lower():
                        item_path = os.path.join(base_dir, item)
                        self.logger.info(f"Found related directory: {item_path}")
                        
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                        else:
                            os.remove(item_path)
                        
                        self.logger.info(f"Removed: {item_path}")
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Could not clean {base_dir}: {e}")
    
    def _cleanup_registry(self, software_info: Dict):
        """Clean Windows registry entries"""
        if self.system != "Windows":
            return
        
        software_name = software_info['name'].lower()
        
        # Registry locations to clean
        reg_locations = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE")
        ]
        
        for hive, path in reg_locations:
            try:
                with winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS) as key:
                    # Enumerate and check subkeys
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            if software_name in subkey_name.lower():
                                winreg.DeleteKey(key, subkey_name)
                                self.logger.info(f"Removed registry key: {subkey_name}")
                            else:
                                i += 1
                        except WindowsError:
                            break
            except Exception:
                continue
    
    def _remove_scheduled_tasks(self, software_info: Dict):
        """Remove scheduled tasks/cron jobs"""
        software_name = software_info['name'].lower()
        
        if self.system == "Windows":
            try:
                # List all scheduled tasks
                result = subprocess.run(["schtasks", "/query", "/fo", "csv"], 
                                      capture_output=True, text=True)
                
                for line in result.stdout.splitlines()[1:]:  # Skip header
                    if software_name in line.lower():
                        task_name = line.split(',')[0].strip('"')
                        subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"])
                        self.logger.info(f"Removed scheduled task: {task_name}")
            except Exception as e:
                self.logger.warning(f"Could not remove scheduled tasks: {e}")
        
        else:  # Linux/macOS
            # Check crontab
            try:
                result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.splitlines()
                    filtered_lines = [l for l in lines if software_name not in l.lower()]
                    
                    if len(filtered_lines) < len(lines):
                        # Update crontab
                        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                            tmp.write('\n'.join(filtered_lines))
                            tmp_path = tmp.name
                        
                        subprocess.run(["crontab", tmp_path])
                        os.unlink(tmp_path)
                        self.logger.info("Removed cron entries")
            except Exception:
                pass

class FileDestroyer:
    """Secure file deletion with DoD standards"""
    
    def __init__(self, logger):
        self.logger = logger
        
    def secure_delete(self, file_path: str, passes: int = SECURE_DELETE_PASSES) -> bool:
        """Securely delete a file with multiple overwrites"""
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
        
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, "ba+", buffering=0) as f:
                for pass_num in range(passes):
                    f.seek(0)
                    
                    # DoD 5220.22-M patterns
                    if pass_num % 3 == 0:
                        # Pass 1: All zeros
                        pattern = b'\x00'
                    elif pass_num % 3 == 1:
                        # Pass 2: All ones
                        pattern = b'\xFF'
                    else:
                        # Pass 3: Random data
                        pattern = os.urandom(1)
                    
                    # Write pattern
                    for _ in range(file_size):
                        f.write(pattern)
                    
                    f.flush()
                    os.fsync(f.fileno())
                    
                    self.logger.info(f"Overwrite pass {pass_num + 1}/{passes} completed")
            
            # Final deletion
            os.remove(file_path)
            self.logger.info(f"File securely deleted: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Secure delete failed: {e}")
            return False
    
    def secure_delete_directory(self, dir_path: str) -> bool:
        """Securely delete a directory and all contents"""
        if not os.path.exists(dir_path):
            self.logger.error(f"Directory not found: {dir_path}")
            return False
        
        try:
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
                        pass
            
            # Remove the main directory
            os.rmdir(dir_path)
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

class TerminalUI:
    """Interactive terminal user interface"""
    
    def __init__(self, scanner, remover, destroyer, logger):
        self.scanner = scanner
        self.remover = remover
        self.destroyer = destroyer
        self.logger = logger
        self.software_list = []
        self.selected_index = 0
        self.page_size = 20
        self.page = 0
        
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
        """Display main menu"""
        print(f"{Fore.GREEN}=== Main Menu ==={Style.RESET_ALL}\n")
        print("1. Scan System Software")
        print("2. Remove Software")
        print("3. File Destroyer")
        print("4. Settings")
        print("5. View Logs")
        print("6. Exit")
        print(f"\n{Fore.YELLOW}⚠️  Use with caution! Always backup important data.{Style.RESET_ALL}")
        
        return input(f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")
    
    def scan_software(self):
        """Scan and display software"""
        print(f"\n{Fore.YELLOW}Scanning system...{Style.RESET_ALL}")
        
        # Progress indicator
        with self.progress_spinner("Scanning"):
            self.software_list = self.scanner.scan_installed_software()
        
        # Sort by name
        self.software_list.sort(key=lambda x: x['name'].lower())
        
        print(f"\n{Fore.GREEN}Found {len(self.software_list)} items{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
    
    def remove_software_menu(self):
        """Software removal interface"""
        if not self.software_list:
            print(f"\n{Fore.RED}No software scanned. Please scan first.{Style.RESET_ALL}")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.show_logo()
            print(f"{Fore.GREEN}=== Remove Software ==={Style.RESET_ALL}\n")
            
            # Display software list with pagination
            start_idx = self.page * self.page_size
            end_idx = min(start_idx + self.page_size, len(self.software_list))
            
            print(f"Page {self.page + 1}/{(len(self.software_list) - 1) // self.page_size + 1}")
            print(f"\n{'#':<5} {'Name':<40} {'Version':<15} {'Size (MB)':<10} {'Type':<15}")
            print("-" * 85)
            
            for i in range(start_idx, end_idx):
                software = self.software_list[i]
                prefix = f"{Fore.YELLOW}>{Style.RESET_ALL}" if i == self.selected_index else " "
                
                print(f"{prefix}{i+1:<4} {software['name'][:39]:<40} "
                      f"{software['version'][:14]:<15} {software['size']:<10} "
                      f"{software['type'][:14]:<15}")
            
            print(f"\n{Fore.CYAN}Commands:{Style.RESET_ALL}")
            print("↑/↓ - Navigate | ←/→ - Change page | r - Remove selected")
            print("f - Force remove | b - Back to menu | q - Quit")
            
            choice = input(f"\n{Fore.CYAN}Enter command: {Style.RESET_ALL}").lower()
            
            if choice == 'b':
                break
            elif choice == 'q':
                sys.exit(0)
            elif choice == 'r':
                self.confirm_and_remove(self.software_list[self.selected_index])
            elif choice == 'f':
                self.confirm_and_remove(self.software_list[self.selected_index], force=True)
            elif choice in ['up', 'down', 'left', 'right']:
                self.navigate(choice)
            else:
                # Try to parse as number
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.software_list):
                        self.selected_index = idx
                        self.page = idx // self.page_size
                except ValueError:
                    pass
    
    def confirm_and_remove(self, software: Dict, force: bool = False):
        """Confirm and remove software"""
        self.clear_screen()
        self.show_logo()
        
        print(f"{Fore.YELLOW}=== Confirm Removal ==={Style.RESET_ALL}\n")
        print(f"Software: {software['name']}")
        print(f"Version: {software['version']}")
        print(f"Type: {software['type']}")
        
        if force:
            print(f"\n{Fore.RED}⚠️  FORCE REMOVAL - Will delete all related files!{Style.RESET_ALL}")
        
        print(f"\n{Fore.RED}This action cannot be undone!{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.CYAN}Type 'YES' to confirm removal: {Style.RESET_ALL}")
        
        if confirm == 'YES':
            print(f"\n{Fore.YELLOW}Removing {software['name']}...{Style.RESET_ALL}")
            
            success = self.remover.remove_software(software, force=force)
            
            if success:
                print(f"\n{Fore.GREEN}✓ Software removed successfully!{Style.RESET_ALL}")
                # Remove from list
                self.software_list.remove(software)
            else:
                print(f"\n{Fore.RED}✗ Removal failed! Check logs for details.{Style.RESET_ALL}")
            
            input("\nPress Enter to continue...")
    
    def file_destroyer_menu(self):
        """File destruction interface"""
        while True:
            self.clear_screen()
            self.show_logo()
            print(f"{Fore.GREEN}=== File Destroyer ==={Style.RESET_ALL}\n")
            print("1. Secure Delete File")
            print("2. Secure Delete Directory")
            print("3. Wipe Free Space")
            print("4. Back to Main Menu")
            
            choice = input(f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")
            
            if choice == '1':
                self.secure_delete_file()
            elif choice == '2':
                self.secure_delete_directory()
            elif choice == '3':
                self.wipe_free_space()
            elif choice == '4':
                break
    
    def secure_delete_file(self):
        """Secure file deletion"""
        self.clear_screen()
        print(f"{Fore.YELLOW}=== Secure File Deletion ==={Style.RESET_ALL}\n")
        
        file_path = input("Enter file path: ").strip()
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"\nFile: {file_path}")
            print(f"Size: {os.path.getsize(file_path) / 1024 / 1024:.2f} MB")
            
            print(f"\n{Fore.RED}⚠️  This will permanently destroy the file!{Style.RESET_ALL}")
            confirm = input(f"\n{Fore.CYAN}Type 'DELETE' to confirm: {Style.RESET_ALL}")
            
            if confirm == 'DELETE':
                print(f"\n{Fore.YELLOW}Securely deleting file...{Style.RESET_ALL}")
                if self.destroyer.secure_delete(file_path):
                    print(f"\n{Fore.GREEN}✓ File securely deleted!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}✗ Deletion failed!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}File not found!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def secure_delete_directory(self):
        """Secure directory deletion"""
        self.clear_screen()
        print(f"{Fore.YELLOW}=== Secure Directory Deletion ==={Style.RESET_ALL}\n")
        
        dir_path = input("Enter directory path: ").strip()
        
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            # Count files
            file_count = sum(len(files) for _, _, files in os.walk(dir_path))
            
            print(f"\nDirectory: {dir_path}")
            print(f"Files: {file_count}")
            
            print(f"\n{Fore.RED}⚠️  This will permanently destroy the directory and all contents!{Style.RESET_ALL}")
            confirm = input(f"\n{Fore.CYAN}Type 'DELETE ALL' to confirm: {Style.RESET_ALL}")
            
            if confirm == 'DELETE ALL':
                print(f"\n{Fore.YELLOW}Securely deleting directory...{Style.RESET_ALL}")
                if self.destroyer.secure_delete_directory(dir_path):
                    print(f"\n{Fore.GREEN}✓ Directory securely deleted!{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}✗ Deletion failed!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}Directory not found!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def wipe_free_space(self):
        """Wipe drive free space"""
        self.clear_screen()
        print(f"{Fore.YELLOW}=== Wipe Free Space ==={Style.RESET_ALL}\n")
        
        if platform.system() == "Windows":
            drive = input("Enter drive letter (e.g., C:): ").strip()
            if not drive.endswith(':'):
                drive += ':'
        else:
            drive = input("Enter mount point (e.g., /home): ").strip()
        
        size_mb = input("Size to wipe in MB (default 100): ").strip()
        size_mb = int(size_mb) if size_mb.isdigit() else 100
        
        print(f"\n{Fore.YELLOW}This will temporarily fill free space to prevent file recovery.{Style.RESET_ALL}")
        confirm = input(f"\n{Fore.CYAN}Continue? (y/n): {Style.RESET_ALL}")
        
        if confirm.lower() == 'y':
            print(f"\n{Fore.YELLOW}Wiping free space...{Style.RESET_ALL}")
            if self.destroyer.wipe_free_space(drive, size_mb):
                print(f"\n{Fore.GREEN}✓ Free space wiped!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}✗ Wipe failed!{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Settings menu"""
        while True:
            self.clear_screen()
            self.show_logo()
            print(f"{Fore.GREEN}=== Settings ==={Style.RESET_ALL}\n")
            
            print(f"1. Dry Run Mode: {Fore.YELLOW}{'ON' if self.remover.dry_run else 'OFF'}{Style.RESET_ALL}")
            print(f"2. Log Level: {Fore.YELLOW}{logging.getLevelName(logging.getLogger().level)}{Style.RESET_ALL}")
            print("3. Clear Logs")
            print("4. Back to Main Menu")
            
            choice = input(f"\n{Fore.CYAN}Select option: {Style.RESET_ALL}")
            
            if choice == '1':
                self.remover.set_dry_run(not self.remover.dry_run)
            elif choice == '2':
                self.change_log_level()
            elif choice == '3':
                self.clear_logs()
            elif choice == '4':
                break
    
    def change_log_level(self):
        """Change logging level"""
        print("\n1. DEBUG")
        print("2. INFO")
        print("3. WARNING")
        print("4. ERROR")
        
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
                        else:
                            print(line.strip())
            else:
                print("No logs found.")
        except Exception as e:
            print(f"Error reading logs: {e}")
        
        input("\nPress Enter to continue...")
    
    def navigate(self, direction: str):
        """Navigate through lists"""
        if direction == 'up':
            self.selected_index = max(0, self.selected_index - 1)
            self.page = self.selected_index // self.page_size
        elif direction == 'down':
            self.selected_index = min(len(self.software_list) - 1, self.selected_index + 1)
            self.page = self.selected_index // self.page_size
        elif direction == 'left':
            self.page = max(0, self.page - 1)
            self.selected_index = self.page * self.page_size
        elif direction == 'right':
            max_page = (len(self.software_list) - 1) // self.page_size
            self.page = min(max_page, self.page + 1)
            self.selected_index = self.page * self.page_size
    
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
                self.thread.join()
                print('\r' + ' ' * (len(self.message) + 10) + '\r', end='')
            
            def _spin(self):
                spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
                i = 0
                while self.running:
                    print(f'\r{self.message} {spinners[i % len(spinners)]}', end='')
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

def main():
    """Main entry point"""
    # Initialize components
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    logger = Logger()
    
    logger.info(f"Starting {APP_NAME} v{VERSION}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Admin privileges: {'Yes' if check_admin() else 'No'}")
    
    # Warning about admin privileges
    if not check_admin():
        print(f"\n{Fore.YELLOW}⚠️  WARNING: Not running with administrator privileges!{Style.RESET_ALL}")
        print("Some features may not work correctly.")
        print("Consider running with sudo (Linux/Mac) or as Administrator (Windows).\n")
        input("Press Enter to continue anyway...")
    
    # Safety warning
    print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.RED}⚠️  IMPORTANT SAFETY WARNING ⚠️{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
    print("\nTerminus is a powerful system administration tool that can:")
    print("- Remove system software and processes")
    print("- Permanently delete files beyond recovery")
    print("- Modify system configurations")
    print("\n⚡ Use this tool ONLY if you understand the risks!")
    print("⚡ Always backup important data before use!")
    print("⚡ Improper use can damage your system!")
    print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
    
    confirm = input(f"\n{Fore.CYAN}Type 'I UNDERSTAND' to continue: {Style.RESET_ALL}")
    
    if confirm != "I UNDERSTAND":
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
    finally:
        logger.info("Terminus shutting down")

if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 10):
        print(f"{Fore.RED}Error: Python 3.10 or higher required{Style.RESET_ALL}")
        sys.exit(1)
    
    main()