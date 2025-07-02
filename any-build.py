#!/usr/bin/env python3
"""
Build Terminus for all platforms with protection
Creates protected executables for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import shutil
import platform
import zipfile
from pathlib import Path
from datetime import datetime

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'

class TerminusBuilder:
    def __init__(self):
        self.current_platform = platform.system()
        self.build_dir = Path("build_all")
        self.output_dir = Path("releases")
        
    def print_banner(self):
        print(f"\n{CYAN}{'='*60}")
        print("  Terminus Multi-Platform Builder")
        print(f"  Building on: {self.current_platform}")
        print(f"{'='*60}{RESET}\n")
        
    def check_requirements(self):
        """Check and install requirements"""
        print(f"{YELLOW}Checking requirements...{RESET}")
        
        required = ['pyinstaller', 'pyarmor']
        
        for package in required:
            try:
                __import__(package)
                print(f"{GREEN}✓ {package} found{RESET}")
            except ImportError:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                
    def clean_build(self):
        """Clean previous builds"""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
            
        self.build_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def protect_code(self):
        """Protect code with PyArmor"""
        print(f"\n{YELLOW}Protecting source code...{RESET}")
        
        protected_dir = self.build_dir / "protected"
        
        cmd = [
            "pyarmor", "gen",
            "--output", str(protected_dir),
            "--private",  # Use private mode
            "--restrict",  # Restrict usage
            "--expired", "2025-12-31",  # Set expiration
            "terminus.py"
        ]
        
        subprocess.check_call(cmd)
        print(f"{GREEN}✓ Code protected{RESET}")
        
        return protected_dir
        
    def build_windows(self, protected_dir):
        """Build Windows executable"""
        print(f"\n{YELLOW}Building Windows executable...{RESET}")
        
        spec_content = '''
# Windows build spec
import sys
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['protected/terminus.py'],
    pathex=['protected'],
    binaries=[],
    datas=[('protected/pyarmor_runtime_*', 'pyarmor_runtime_*')],
    hiddenimports=['psutil', 'colorama', 'win32api', 'win32security'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['test', 'pytest'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='terminus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon='terminus.ico' if os.path.exists('terminus.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
        
        spec_file = self.build_dir / "terminus_win.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        # Create version info
        version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'Terminus System Manager'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'terminus'),
        StringStruct(u'LegalCopyright', u'Copyright 2024'),
        StringStruct(u'OriginalFilename', u'terminus.exe'),
        StringStruct(u'ProductName', u'Terminus'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        with open(self.build_dir / "version_info.txt", 'w') as f:
            f.write(version_info)
            
        # Build
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--workpath", str(self.build_dir / "work_win"),
            "--distpath", str(self.output_dir / "windows"),
            str(spec_file)
        ]
        
        subprocess.check_call(cmd)
        print(f"{GREEN}✓ Windows build complete{RESET}")
        
    def build_linux(self, protected_dir):
        """Build Linux executable"""
        print(f"\n{YELLOW}Building Linux executable...{RESET}")
        
        spec_content = '''
# Linux build spec
a = Analysis(
    ['protected/terminus.py'],
    pathex=['protected'],
    binaries=[],
    datas=[('protected/pyarmor_runtime_*', 'pyarmor_runtime_*')],
    hiddenimports=['psutil', 'colorama'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['test', 'pytest'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='terminus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
)
'''
        
        spec_file = self.build_dir / "terminus_linux.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        # Build
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--workpath", str(self.build_dir / "work_linux"),
            "--distpath", str(self.output_dir / "linux"),
            str(spec_file)
        ]
        
        subprocess.check_call(cmd)
        
        # Make executable
        os.chmod(self.output_dir / "linux" / "terminus", 0o755)
        
        print(f"{GREEN}✓ Linux build complete{RESET}")
        
    def build_macos(self, protected_dir):
        """Build macOS executable"""
        print(f"\n{YELLOW}Building macOS executable...{RESET}")
        
        spec_content = '''
# macOS build spec
a = Analysis(
    ['protected/terminus.py'],
    pathex=['protected'],
    binaries=[],
    datas=[('protected/pyarmor_runtime_*', 'pyarmor_runtime_*')],
    hiddenimports=['psutil', 'colorama'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['test', 'pytest'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='terminus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # UPX often causes issues on macOS
    console=True,
    argv_emulation=False,
    target_arch='universal2',  # Support both Intel and Apple Silicon
)

app = BUNDLE(
    exe,
    name='Terminus.app',
    icon='terminus.icns' if os.path.exists('terminus.icns') else None,
    bundle_identifier='com.yourcompany.terminus',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
    },
)
'''
        
        spec_file = self.build_dir / "terminus_macos.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
            
        # Build
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--workpath", str(self.build_dir / "work_macos"),
            "--distpath", str(self.output_dir / "macos"),
            str(spec_file)
        ]
        
        subprocess.check_call(cmd)
        print(f"{GREEN}✓ macOS build complete{RESET}")
        
    def create_packages(self):
        """Create distribution packages for each platform"""
        print(f"\n{YELLOW}Creating distribution packages...{RESET}")
        
        timestamp = datetime.now().strftime("%Y%m%d")
        
        # Windows package
        if (self.output_dir / "windows" / "terminus.exe").exists():
            self.create_zip_package(
                self.output_dir / "windows",
                f"terminus_windows_{timestamp}.zip",
                "windows"
            )
            
        # Linux package
        if (self.output_dir / "linux" / "terminus").exists():
            self.create_zip_package(
                self.output_dir / "linux",
                f"terminus_linux_{timestamp}.zip",
                "linux"
            )
            
        # macOS package
        if (self.output_dir / "macos" / "Terminus.app").exists():
            self.create_zip_package(
                self.output_dir / "macos",
                f"terminus_macos_{timestamp}.zip",
                "macos"
            )
            
    def create_zip_package(self, source_dir, package_name, platform_name):
        """Create a ZIP package with all necessary files"""
        
        # Create platform-specific README
        readme_content = f'''
Terminus - {platform_name.title()} Edition
=====================================

Installation:
------------
{"1. Extract all files\n2. Run terminus.exe as Administrator" if platform_name == "windows" else 
 "1. Extract all files\n2. chmod +x terminus\n3. Run ./terminus with sudo" if platform_name == "linux" else
 "1. Extract all files\n2. Move Terminus.app to Applications\n3. Run with admin privileges"}

First Run:
---------
1. The program will display your Machine ID
2. Email the Machine ID to: admin@example.com
3. You will receive a license key
4. Enter the license key when prompted

Support:
-------
Email: support@example.com
Web: https://example.com/terminus

This software is protected by copyright.
Unauthorized distribution is prohibited.
'''
        
        # Create temp directory for package
        temp_pkg = self.build_dir / f"pkg_{platform_name}"
        temp_pkg.mkdir(exist_ok=True)
        
        # Copy files
        if platform_name == "windows":
            shutil.copy2(source_dir / "terminus.exe", temp_pkg)
        elif platform_name == "linux":
            shutil.copy2(source_dir / "terminus", temp_pkg)
        elif platform_name == "macos":
            shutil.copytree(source_dir / "Terminus.app", temp_pkg / "Terminus.app")
            
        # Add README
        with open(temp_pkg / "README.txt", 'w') as f:
            f.write(readme_content)
            
        # Add LICENSE if exists
        if Path("LICENSE").exists():
            shutil.copy2("LICENSE", temp_pkg / "LICENSE.txt")
            
        # Create ZIP
        with zipfile.ZipFile(self.output_dir / package_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in temp_pkg.rglob('*'):
                if file.is_file():
                    zf.write(file, file.relative_to(temp_pkg))
                    
        print(f"{GREEN}✓ Created {package_name}{RESET}")
        
    def build_current_platform(self):
        """Build only for current platform"""
        protected_dir = self.protect_code()
        
        if self.current_platform == "Windows":
            self.build_windows(protected_dir)
        elif self.current_platform == "Linux":
            self.build_linux(protected_dir)
        elif self.current_platform == "Darwin":
            self.build_macos(protected_dir)
        else:
            print(f"{RED}Unsupported platform: {self.current_platform}{RESET}")
            
    def build_all(self):
        """Build for all platforms (requires cross-compilation setup)"""
        protected_dir = self.protect_code()
        
        # Note: Cross-compilation requires platform-specific tools
        print(f"\n{YELLOW}Note: Building for all platforms from {self.current_platform}{RESET}")
        print("For best results, build on each target platform")
        
        # Build for current platform
        self.build_current_platform()
        
        print(f"\n{YELLOW}To build for other platforms:{RESET}")
        print("- Windows: Run this script on Windows")
        print("- Linux: Run this script on Linux")
        print("- macOS: Run this script on macOS")
        
    def run(self):
        """Main build process"""
        self.print_banner()
        
        if not Path("terminus.py").exists():
            print(f"{RED}Error: terminus.py not found!{RESET}")
            return
            
        self.check_requirements()
        self.clean_build()
        
        # Ask user what to build
        print(f"\n{CYAN}Build Options:{RESET}")
        print("1. Current platform only")
        print("2. All platforms (requires manual builds)")
        
        choice = input("\nSelect option (1/2): ").strip()
        
        if choice == "1":
            self.build_current_platform()
        else:
            self.build_all()
            
        self.create_packages()
        
        print(f"\n{GREEN}{'='*60}")
        print("Build Complete!")
        print(f"{'='*60}{RESET}")
        print(f"\nOutput directory: {self.output_dir}")
        print("\nPackages created:")
        for package in self.output_dir.glob("*.zip"):
            print(f"- {package.name}")

if __name__ == "__main__":
    builder = TerminusBuilder()
    try:
        builder.run()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Build cancelled{RESET}")
    except Exception as e:
        print(f"\n{RED}Build failed: {e}{RESET}")
        import traceback
        traceback.print_exc()