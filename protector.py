#!/usr/bin/env python3
"""
Simple Terminus Protection Script using PyArmor
Provides strong code obfuscation and licensing
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_banner():
    print(f"\n{CYAN}{'='*50}")
    print("  Terminus Code Protection - Simple Method")
    print(f"{'='*50}{RESET}\n")

def install_pyarmor():
    """Install PyArmor for code protection"""
    try:
        import pyarmor
        print(f"{GREEN}✓ PyArmor is installed{RESET}")
        return True
    except ImportError:
        print(f"{YELLOW}Installing PyArmor...{RESET}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyarmor"])
            print(f"{GREEN}✓ PyArmor installed successfully{RESET}")
            return True
        except:
            print(f"{RED}Failed to install PyArmor{RESET}")
            return False

def protect_with_pyarmor():
    """Use PyArmor to obfuscate and protect the code"""
    print(f"\n{BLUE}Protecting code with PyArmor...{RESET}")
    
    # Create output directory
    output_dir = Path("protected_terminus")
    output_dir.mkdir(exist_ok=True)
    
    # Basic PyArmor protection
    cmd = [
        "pyarmor", "gen",
        "--output", str(output_dir),
        "--restrict",  # Restrict to specific machines
        "--assert-call",  # Add protection calls
        "--assert-import",  # Protect imports
        "terminus.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"{GREEN}✓ Code protected successfully{RESET}")
        
        # Create launcher script
        launcher_content = '''#!/usr/bin/env python3
"""Protected Terminus Launcher"""
import sys
import os

# Add pyarmor runtime to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run protected module
from terminus import main

if __name__ == "__main__":
    main()
'''
        
        with open(output_dir / "run_terminus.py", 'w') as f:
            f.write(launcher_content)
            
        # Make executable on Unix
        if platform.system() != 'Windows':
            os.chmod(output_dir / "run_terminus.py", 0o755)
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{RED}Protection failed: {e}{RESET}")
        return False

def create_pyinstaller_bundle():
    """Create a standalone executable with PyInstaller"""
    print(f"\n{BLUE}Creating standalone executable...{RESET}")
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print(f"{YELLOW}Installing PyInstaller...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create spec file for better control
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['protected_terminus/run_terminus.py'],
    pathex=['protected_terminus'],
    binaries=[],
    datas=[('protected_terminus/pyarmor_runtime_*', 'pyarmor_runtime_*')],
    hiddenimports=['psutil', 'colorama'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='terminus_protected',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open("terminus_protected.spec", 'w') as f:
        f.write(spec_content)
    
    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "terminus_protected.spec"
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"{GREEN}✓ Executable created successfully{RESET}")
        return True
    except:
        print(f"{RED}Failed to create executable{RESET}")
        return False

def create_license_generator():
    """Create a license key generator"""
    generator_code = '''#!/usr/bin/env python3
"""
License Generator for Protected Terminus
Run this on your machine to generate licenses for customers
"""

import hashlib
import json
import base64
from datetime import datetime, timedelta
import sys

def generate_license(machine_id, days=30, features="full"):
    """Generate a license for a specific machine"""
    
    expiry = datetime.now() + timedelta(days=days)
    
    license_data = {
        "machine_id": machine_id,
        "expiry": expiry.isoformat(),
        "features": features,
        "version": "1.0.0"
    }
    
    # Create signature (in production, use proper cryptography)
    signature = hashlib.sha256(
        json.dumps(license_data, sort_keys=True).encode()
    ).hexdigest()
    
    license_data["signature"] = signature
    
    # Encode license
    license_key = base64.b64encode(
        json.dumps(license_data).encode()
    ).decode()
    
    # Format for readability
    formatted = '-'.join([license_key[i:i+5] for i in range(0, len(license_key), 5)])
    
    return formatted

def main():
    print("Terminus License Generator")
    print("=" * 30)
    
    machine_id = input("Enter customer machine ID: ")
    days = input("License duration (days) [30]: ") or "30"
    
    try:
        days = int(days)
    except:
        print("Invalid duration, using 30 days")
        days = 30
    
    license_key = generate_license(machine_id, days)
    
    print(f"\\nGenerated License Key:")
    print("=" * 50)
    print(license_key)
    print("=" * 50)
    
    print(f"\\nValid for {days} days")
    print(f"Machine ID: {machine_id}")
    
    # Save to file
    with open(f"license_{machine_id[:8]}.key", 'w') as f:
        f.write(license_key)
    
    print(f"\\nLicense saved to: license_{machine_id[:8]}.key")

if __name__ == "__main__":
    main()
'''
    
    with open("generate_license.py", 'w') as f:
        f.write(generator_code)
    
    print(f"{GREEN}✓ License generator created: generate_license.py{RESET}")

def create_distribution_package():
    """Create final distribution package"""
    print(f"\n{BLUE}Creating distribution package...{RESET}")
    
    dist_dir = Path("dist_protected")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy necessary files
    files_to_include = [
        ("dist/terminus_protected.exe" if platform.system() == "Windows" else "dist/terminus_protected", 
         "terminus.exe" if platform.system() == "Windows" else "terminus"),
        ("README.md", "README.txt"),
        ("LICENSE", "LICENSE.txt")
    ]
    
    for src, dst in files_to_include:
        if os.path.exists(src):
            shutil.copy2(src, dist_dir / dst)
    
    # Create install instructions
    install_instructions = f'''
Terminus - Protected Edition
============================

Installation Instructions:
-------------------------
1. {"Run terminus.exe as Administrator" if platform.system() == "Windows" else "Run ./terminus with sudo"}
2. On first run, the program will display your Machine ID
3. Send the Machine ID to admin@example.com to receive your license
4. Enter the license when prompted

System Requirements:
-------------------
- {"Windows 10 or later" if platform.system() == "Windows" else "Linux kernel 3.10+" if platform.system() == "Linux" else "macOS 10.15+"}
- Administrator/root privileges
- 100MB free disk space

Support:
--------
Email: support@example.com
License: admin@example.com

This software is protected by copyright law.
Unauthorized distribution or reverse engineering is prohibited.
'''
    
    with open(dist_dir / "INSTALL.txt", 'w') as f:
        f.write(install_instructions)
    
    print(f"{GREEN}✓ Distribution package created in: {dist_dir}{RESET}")

def main():
    print_banner()
    
    # Check if terminus.py exists
    if not os.path.exists("terminus.py"):
        print(f"{RED}Error: terminus.py not found!{RESET}")
        print("Run this script in the Terminus directory.")
        sys.exit(1)
    
    # Install PyArmor
    if not install_pyarmor():
        print(f"{RED}Cannot proceed without PyArmor{RESET}")
        sys.exit(1)
    
    # Protect code
    if not protect_with_pyarmor():
        print(f"{RED}Code protection failed{RESET}")
        sys.exit(1)
    
    # Create executable
    create_pyinstaller_bundle()
    
    # Create license generator
    create_license_generator()
    
    # Create distribution
    create_distribution_package()
    
    print(f"\n{GREEN}{'='*50}")
    print("Protection Complete!")
    print(f"{'='*50}{RESET}")
    print("\nProtected files:")
    print(f"- Obfuscated code: protected_terminus/")
    print(f"- Standalone executable: dist/terminus_protected")
    print(f"- License generator: generate_license.py")
    print(f"- Distribution package: dist_protected/")
    
    print(f"\n{YELLOW}Next steps:{RESET}")
    print("1. Test the protected executable")
    print("2. Use generate_license.py to create licenses")
    print("3. Distribute files from dist_protected/")

if __name__ == "__main__":
    main()