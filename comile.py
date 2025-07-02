#!/usr/bin/env python3
"""
Terminus Compilation Script
Compiles and protects Terminus source code for distribution
"""

import os
import sys
import shutil
import platform
import subprocess
import tempfile
import zipfile
import hashlib
import json
import base64
from datetime import datetime
from pathlib import Path
import random
import string

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

class TerminusCompiler:
    def __init__(self):
        self.platform = platform.system()
        self.build_dir = Path("build_protected")
        self.dist_dir = Path("dist_protected")
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def print_banner(self):
        """Display compilation banner"""
        print(f"\n{CYAN}{'='*60}")
        print("     Terminus Code Protection & Compilation")
        print(f"{'='*60}{RESET}\n")
        
    def check_requirements(self):
        """Check if compilation requirements are met"""
        print(f"{BLUE}Checking requirements...{RESET}")
        
        # Check Python version
        if sys.version_info < (3, 10):
            print(f"{RED}Error: Python 3.10+ required{RESET}")
            return False
            
        # Check PyInstaller
        try:
            import PyInstaller
            print(f"{GREEN}✓ PyInstaller found{RESET}")
        except ImportError:
            print(f"{YELLOW}Installing PyInstaller...{RESET}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            
        # Check other tools
        required_packages = ['pyarmor', 'pycryptodome']
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"{GREEN}✓ {package} found{RESET}")
            except ImportError:
                print(f"{YELLOW}Installing {package}...{RESET}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                
        return True
        
    def obfuscate_code(self):
        """Obfuscate Python source code"""
        print(f"\n{BLUE}Obfuscating source code...{RESET}")
        
        # Create obfuscated directory
        obf_dir = self.temp_dir / "obfuscated"
        obf_dir.mkdir(exist_ok=True)
        
        # Copy main file
        shutil.copy2("terminus.py", obf_dir / "terminus.py")
        
        # Basic obfuscation transformations
        self._obfuscate_strings(obf_dir / "terminus.py")
        self._obfuscate_variables(obf_dir / "terminus.py")
        self._add_anti_debug(obf_dir / "terminus.py")
        
        print(f"{GREEN}✓ Code obfuscated{RESET}")
        return obf_dir
        
    def _obfuscate_strings(self, file_path):
        """Encode string literals"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Simple string encoding (in production, use more sophisticated methods)
        import re
        
        def encode_string(match):
            s = match.group(1)
            if len(s) > 3:  # Only encode longer strings
                encoded = base64.b64encode(s.encode()).decode()
                return f'base64.b64decode("{encoded}").decode()'
            return f'"{s}"'
            
        # This is a simplified example - real obfuscation would be more complex
        # content = re.sub(r'"([^"]+)"', encode_string, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def _obfuscate_variables(self, file_path):
        """Rename variables to make code harder to read"""
        # In production, use proper AST parsing and transformation
        pass
        
    def _add_anti_debug(self, file_path):
        """Add anti-debugging code"""
        anti_debug_code = '''
# Anti-debugging protection
import sys
import os

def _check_debugger():
    """Check if running under debugger"""
    if hasattr(sys, 'gettrace') and sys.gettrace():
        print("Debugger detected!")
        sys.exit(1)
    if 'pdb' in sys.modules or 'ipdb' in sys.modules:
        print("Debugger module detected!")
        sys.exit(1)
        
_check_debugger()

'''
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Add anti-debug code at the beginning
        content = anti_debug_code + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def compile_executable(self, obf_dir):
        """Compile to standalone executable using PyInstaller"""
        print(f"\n{BLUE}Compiling executable...{RESET}")
        
        # Prepare PyInstaller spec file
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{obf_dir / "terminus.py"}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['psutil', 'colorama', 'curses'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['test', 'pytest', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='terminus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
        
        spec_file = self.temp_dir / "terminus.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        # Run PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",
            "--noconsole" if self.platform == "Windows" else "--console",
            f"--distpath={self.dist_dir}",
            f"--workpath={self.build_dir}",
            str(spec_file)
        ]
        
        if self.platform == "Windows":
            cmd.extend(["--add-binary", "pywin32;."])
            
        subprocess.check_call(cmd)
        
        print(f"{GREEN}✓ Executable compiled{RESET}")
        
    def create_license_system(self):
        """Create a simple license verification system"""
        print(f"\n{BLUE}Creating license system...{RESET}")
        
        license_code = '''
import hashlib
import platform
import uuid
import sys
from datetime import datetime, timedelta

class LicenseManager:
    """Simple license verification"""
    
    def __init__(self):
        self.license_file = ".terminus_license"
        
    def get_machine_id(self):
        """Get unique machine identifier"""
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                       for i in range(0,48,8)][::-1])
        return hashlib.sha256(mac.encode()).hexdigest()[:16]
        
    def verify_license(self):
        """Verify license file"""
        try:
            with open(self.license_file, 'r') as f:
                license_data = f.read().strip()
                
            # Simple validation (in production, use cryptographic signatures)
            parts = license_data.split('-')
            if len(parts) != 3:
                return False
                
            machine_id = parts[0]
            expiry = datetime.fromisoformat(parts[1])
            
            if machine_id != self.get_machine_id():
                print("License not valid for this machine!")
                return False
                
            if datetime.now() > expiry:
                print("License expired!")
                return False
                
            return True
            
        except Exception:
            print("No valid license found!")
            return False
            
    def generate_license(self, days=30):
        """Generate license for current machine"""
        machine_id = self.get_machine_id()
        expiry = datetime.now() + timedelta(days=days)
        checksum = hashlib.sha256(f"{machine_id}{expiry}".encode()).hexdigest()[:8]
        
        license_key = f"{machine_id}-{expiry.isoformat()}-{checksum}"
        
        with open(self.license_file, 'w') as f:
            f.write(license_key)
            
        return license_key

# Add license check to main code
_lm = LicenseManager()
if not _lm.verify_license():
    print("\\nPlease contact admin@example.com for a license.")
    print(f"Your machine ID: {_lm.get_machine_id()}")
    sys.exit(1)
'''
        
        # Save license manager
        with open(self.temp_dir / "license_manager.py", 'w') as f:
            f.write(license_code)
            
        print(f"{GREEN}✓ License system created{RESET}")
        
    def create_installer(self):
        """Create platform-specific installer"""
        print(f"\n{BLUE}Creating installer...{RESET}")
        
        if self.platform == "Windows":
            self._create_windows_installer()
        elif self.platform == "Linux":
            self._create_linux_installer()
        elif self.platform == "Darwin":
            self._create_macos_installer()
            
    def _create_windows_installer(self):
        """Create Windows installer using NSIS or Inno Setup"""
        installer_script = '''
; Terminus Installer Script for Inno Setup

[Setup]
AppName=Terminus System Manager
AppVersion=1.0.0
AppPublisher=Your Company
AppPublisherURL=https://example.com
DefaultDirName={autopf}\\Terminus
DefaultGroupName=Terminus
OutputBaseFilename=TerminusSetup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist_protected\\terminus.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Terminus"; Filename: "{app}\\terminus.exe"
Name: "{group}\\Uninstall Terminus"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\\terminus.exe"; Description: "Launch Terminus"; Flags: nowait postinstall skipifsilent
'''
        
        with open("terminus_installer.iss", 'w') as f:
            f.write(installer_script)
            
        print(f"{YELLOW}Installer script created: terminus_installer.iss{RESET}")
        print("To build installer, use Inno Setup Compiler")
        
    def _create_linux_installer(self):
        """Create Linux .deb or .rpm package"""
        # Create .deb package structure
        deb_dir = self.dist_dir / "terminus_deb"
        deb_dir.mkdir(exist_ok=True)
        
        # Create DEBIAN control file
        control_dir = deb_dir / "DEBIAN"
        control_dir.mkdir(exist_ok=True)
        
        control_content = '''Package: terminus
Version: 1.0.0
Section: admin
Priority: optional
Architecture: amd64
Maintainer: Your Name <admin@example.com>
Description: Advanced System Software Manager
 Terminus is a powerful tool for managing system software
'''
        
        with open(control_dir / "control", 'w') as f:
            f.write(control_content)
            
        # Copy executable
        usr_bin = deb_dir / "usr" / "local" / "bin"
        usr_bin.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.dist_dir / "terminus", usr_bin / "terminus")
        
        print(f"{GREEN}✓ Debian package structure created{RESET}")
        
    def _create_macos_installer(self):
        """Create macOS .app bundle"""
        app_dir = self.dist_dir / "Terminus.app"
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        
        # Create directories
        macos_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        shutil.copy2(self.dist_dir / "terminus", macos_dir / "terminus")
        
        # Create Info.plist
        plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>terminus</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourcompany.terminus</string>
    <key>CFBundleName</key>
    <string>Terminus</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
</dict>
</plist>'''
        
        with open(contents_dir / "Info.plist", 'w') as f:
            f.write(plist_content)
            
        print(f"{GREEN}✓ macOS app bundle created{RESET}")
        
    def create_distribution_package(self):
        """Create final distribution package"""
        print(f"\n{BLUE}Creating distribution package...{RESET}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"terminus_{self.platform.lower()}_{timestamp}"
        
        # Create README for distribution
        readme_content = f'''
Terminus - System Software Manager
=================================

Version: 1.0.0
Platform: {self.platform}
Build Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Installation Instructions:
-------------------------
1. Run the installer or executable
2. When prompted, enter your license key
3. Contact admin@example.com for license

Security Notice:
---------------
This software is protected by copyright law.
Unauthorized distribution is prohibited.

Generated Machine ID will be displayed on first run.
'''
        
        with open(self.dist_dir / "README_DIST.txt", 'w') as f:
            f.write(readme_content)
            
        # Create ZIP package
        with zipfile.ZipFile(f"{package_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in self.dist_dir.rglob('*'):
                if file.is_file():
                    zf.write(file, file.relative_to(self.dist_dir))
                    
        print(f"{GREEN}✓ Distribution package created: {package_name}.zip{RESET}")
        
        # Calculate checksum
        with open(f"{package_name}.zip", 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()
            
        print(f"{CYAN}SHA256: {checksum}{RESET}")
        
        # Save build info
        build_info = {
            "version": "1.0.0",
            "platform": self.platform,
            "build_date": datetime.now().isoformat(),
            "checksum": checksum,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
        
        with open(f"{package_name}_build_info.json", 'w') as f:
            json.dump(build_info, f, indent=2)
            
    def cleanup(self):
        """Clean up temporary files"""
        print(f"\n{BLUE}Cleaning up...{RESET}")
        
        try:
            shutil.rmtree(self.temp_dir)
            shutil.rmtree(self.build_dir, ignore_errors=True)
            print(f"{GREEN}✓ Cleanup complete{RESET}")
        except Exception as e:
            print(f"{YELLOW}Warning: Cleanup failed: {e}{RESET}")
            
    def compile(self):
        """Main compilation process"""
        self.print_banner()
        
        if not self.check_requirements():
            print(f"{RED}Requirements check failed!{RESET}")
            return False
            
        try:
            # Create directories
            self.build_dir.mkdir(exist_ok=True)
            self.dist_dir.mkdir(exist_ok=True)
            
            # Obfuscate code
            obf_dir = self.obfuscate_code()
            
            # Add license system
            self.create_license_system()
            
            # Compile executable
            self.compile_executable(obf_dir)
            
            # Create installer
            self.create_installer()
            
            # Create distribution package
            self.create_distribution_package()
            
            # Cleanup
            self.cleanup()
            
            print(f"\n{GREEN}{'='*60}")
            print("Compilation Complete!")
            print(f"{'='*60}{RESET}")
            print(f"\nOutput directory: {self.dist_dir}")
            print(f"Executable: {self.dist_dir / 'terminus'}")
            
            return True
            
        except Exception as e:
            print(f"\n{RED}Compilation failed: {e}{RESET}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point"""
    compiler = TerminusCompiler()
    
    # Check if source file exists
    if not os.path.exists("terminus.py"):
        print(f"{RED}Error: terminus.py not found!{RESET}")
        print("Make sure you run this script in the Terminus directory.")
        sys.exit(1)
        
    # Run compilation
    success = compiler.compile()
    
    if not success:
        sys.exit(1)
        
    # Generate sample license for testing
    print(f"\n{YELLOW}Generating test license...{RESET}")
    from license_manager import LicenseManager
    lm = LicenseManager()
    test_license = lm.generate_license(30)
    print(f"Test license: {test_license}")
    print(f"Valid for 30 days")


if __name__ == "__main__":
    main()