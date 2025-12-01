# 🔥 Terminus: The Ultimate System Cleaner v5.0 ULTIMATE 🔥

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██╗   ██╗███████╗    ║
║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██║   ██║██╔════╝    ║
║     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║███████╗    ║
║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║╚════██║    ║
║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████║    ║
║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ║
║                                                                           ║
║  ⚡ ULTIMATE SYSTEM CLEANER - REMOVES EVERYTHING ⚡                      ║
║  Version 5.0 ULTIMATE - Cross-Platform Power Tool                        ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**Terminus** isn't just another uninstaller - it's the digital equivalent of a **surgical strike** against stubborn software and sensitive files. When regular removal tools fail, Terminus succeeds with military-grade precision and beautiful terminal UI.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OS](https://img.shields.io/badge/os-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-5.0%20ULTIMATE-brightgreen.svg)](https://github.com/sarat1kyan/Terminus)

---

## 🌟 Features That Pack a Punch

| Capability | Description | Status |
|------------|-------------|--------|
| **💣 Nuclear Uninstallation** | Remove ANY software, no matter how deeply entrenched | ✅ Enhanced |
| **🔥 Forensic File Destruction** | 7-pass secure wipe (DoD 5220.22-M + Gutmann patterns) | ✅ Enhanced |
| **🛡️ Resistance Breaker** | Bypasses anti-uninstall protections and process locks | ✅ Enhanced |
| **🔍 System-Wide Scanning** | Comprehensive detection across all package managers | ✅ Enhanced |
| **🎨 Beautiful Terminal UI** | Stunning interface with progress bars and animations | ✅ New |
| **🌐 Cross-Platform** | Works on Windows, Linux, and macOS | ✅ Enhanced |
| **⚡ Ultra-Force Removal** | Multiple deletion methods per OS | ✅ New |
| **📊 Real-Time Progress** | Visual feedback with progress bars and spinners | ✅ New |

---

## 🚀 Quick Start

### One-Command Installation

**Windows:**
```powershell
# PowerShell (Recommended)
.\install.ps1

# Or Batch Script
install.bat

# Or Python Installer
python install.py
```

**Linux/macOS:**
```bash
# Make executable and run
chmod +x install.sh
./install.sh

# Or Python Installer
python3 install.py
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/sarat1kyan/terminus.git
cd terminus

# Install dependencies
pip install psutil colorama

# Windows only
pip install pywin32 windows-curses

# Run Terminus
python terminus.py
```

---

## 📋 Installation Scripts Explained

### Installation Scripts (Run Once)

| Script | Platform | Purpose |
|--------|----------|---------|
| `install.sh` | Linux/macOS | Installs dependencies, creates directories, verifies setup |
| `install.ps1` | Windows | PowerShell installer with dependency checking |
| `install.bat` | Windows | Batch script alternative for Windows |
| `install.py` | All | Cross-platform Python installer |

**Recommendation:** Use the platform-specific installer (`install.sh` or `install.ps1`) for the best experience.

### Launcher Scripts (Run Every Time)

| Script | Platform | Purpose |
|--------|----------|---------|
| `terminus.sh` | Linux/macOS | Launches Terminus with dependency checks and privilege warnings |
| `terminus.ps1` | Windows | PowerShell launcher with admin check and dependency installation |
| `terminus.bat` | Windows | Simple batch launcher for quick access |

**Recommendation:** Use launcher scripts instead of running `terminus.py` directly - they handle dependencies and provide better error messages.

---

## 🖥️ Platform-Specific Setup

### Windows

**Requirements:**
- Windows 10/11 or Windows Server 2016+
- Python 3.10+ ([Download](https://www.python.org/downloads/))
- PowerShell 5.0+ (usually pre-installed)

**Installation:**
```powershell
# Run installer
.\install.ps1

# Or use batch script
install.bat
```

**Running:**
```powershell
# Recommended: Use launcher script
.\terminus.ps1

# Or batch launcher
.\terminus.bat

# Or direct execution
python terminus.py
```

**Windows-Specific Features:**
- ✅ Registry cleaning (HKLM/HKCU)
- ✅ System restore point creation
- ✅ Windows service removal
- ✅ Scheduled task elimination
- ✅ Windows Store/UWP app removal
- ✅ Multiple deletion methods (PowerShell, takeown, robocopy trick)

### Linux

**Requirements:**
- Linux kernel 3.10+
- Python 3.10+
- sudo/root access for system operations

**Installation:**
```bash
# Run installer
chmod +x install.sh
./install.sh
```

**Running:**
```bash
# Recommended: Use launcher script
./terminus.sh

# Or direct execution
python3 terminus.py

# With root privileges (for system operations)
sudo ./terminus.sh
```

**Supported Package Managers:**
- ✅ APT (Debian/Ubuntu)
- ✅ YUM/DNF (RHEL/CentOS/Fedora)
- ✅ Pacman (Arch Linux)
- ✅ Zypper (openSUSE)
- ✅ Snap
- ✅ Flatpak
- ✅ AppImage detection
- ✅ Portage (Gentoo)

### macOS

**Requirements:**
- macOS 10.15 (Catalina) or newer
- Python 3.10+
- Admin password for sudo operations

**Installation:**
```bash
# Run installer
chmod +x install.sh
./install.sh
```

**Running:**
```bash
# Recommended: Use launcher script
./terminus.sh

# Or direct execution
python3 terminus.py

# With admin privileges
sudo ./terminus.sh
```

**macOS-Specific Features:**
- ✅ .app bundle removal
- ✅ Homebrew integration (packages and casks)
- ✅ MacPorts support
- ✅ Launch agent cleanup
- ✅ Preference file deletion
- ✅ Multiple application directory scanning

---

## 🎯 Usage Guide

### First Time Setup

1. **Install Dependencies:**
   ```bash
   # Run the appropriate installer
   ./install.sh      # Linux/macOS
   .\install.ps1      # Windows PowerShell
   install.bat        # Windows Batch
   ```

2. **Launch Terminus:**
   ```bash
   ./terminus.sh      # Linux/macOS
   .\terminus.ps1     # Windows
   ```

3. **Start with Scanning:**
   - Select option `1` - Scan System Software
   - Wait for scan to complete
   - Review detected software

4. **Enable Safety Mode:**
   - Go to Settings (option `4`)
   - Enable "Dry Run Mode" to test without actual deletion

### Removing Software

1. **Scan First:** Always scan before removing
2. **Select Software:** Navigate with arrow keys, select with Enter
3. **Choose Method:**
   - **Standard Removal:** Uses uninstaller if available
   - **Force Removal (F):** Aggressive multi-method deletion
4. **Confirm:** Type `YES` to confirm (case-sensitive)

### Secure File Deletion

1. **Select File Destroyer:** Option `3` from main menu
2. **Choose Operation:**
   - Secure Delete File: 7-pass wipe
   - Secure Delete Directory: Recursive secure deletion
   - Wipe Free Space: Overwrite free space
3. **Confirm:** Type `DELETE` or `DELETE ALL` to confirm

---

## 🛡️ Safety & Best Practices

### ⚠️ Critical Warnings

**Before using Terminus:**

1. **✅ Create Backups**
   ```bash
   # Windows: Create system restore point
   # Linux: Use rsync or backup tool
   # macOS: Use Time Machine
   ```

2. **✅ Test in Virtual Machine**
   - Install VirtualBox/VMware
   - Create snapshot before testing
   - Practice removal operations safely

3. **✅ Document Your System**
   ```bash
   # Windows
   wmic product get name,version > software_list.txt
   
   # Linux
   dpkg -l > software_list.txt
   
   # macOS
   brew list --versions > brew_list.txt
   ```

### ☠️ Never Remove These

| Platform | Protected Components | Consequences |
|----------|---------------------|--------------|
| **Windows** | Defender, .NET, DirectX, KB updates | ⚠️ System instability |
| **Linux** | Kernel, libc, systemd, coreutils | 💥 Unbootable system |
| **macOS** | System frameworks, kexts, security | 🚫 Loss of core functions |

### 🆘 Emergency Recovery

**Windows:**
1. Boot from installation media
2. Select "Repair your computer"
3. Choose Troubleshoot → Advanced Options
4. Run: `sfc /scannow`
5. Use System Restore if available

**Linux:**
1. Boot from Live USB
2. Mount root partition: `mount /dev/sda1 /mnt`
3. Chroot: `chroot /mnt`
4. Reinstall packages: `apt install --reinstall coreutils systemd`
5. Update bootloader: `update-grub`

**macOS:**
1. Reboot holding Cmd+R
2. Open Disk Utility → Repair Disk
3. Reinstall macOS without losing data
4. Restore from Time Machine backup

---

## 🛠️ Technical Details

### Secure Deletion

Terminus uses **7-pass secure deletion** following:
- **DoD 5220.22-M** standard
- **Gutmann method** patterns
- **Random data** overwrites
- **File renaming** before deletion

### Removal Methods

**Windows:**
- Standard uninstaller execution
- PowerShell `Remove-Item -Force -Recurse`
- `takeown` + `icacls` + deletion
- Robocopy mirror trick
- Boot-time deletion scheduling

**Linux/macOS:**
- Package manager removal
- `chattr` to remove immutable flags
- `shred` for secure file deletion
- `find -delete` for recursive removal
- `lsof` + `kill` for locked files

### Performance

| Operation | Time Range | CPU Usage | Disk I/O |
|-----------|------------|-----------|----------|
| System Scan | 2-10 minutes | Medium | Low |
| Standard Removal | 1-5 minutes | Medium | Medium |
| Secure File Wipe | 5-15+ minutes | High | Very High |
| Registry Cleanup | 1-10 minutes | Low | Medium |

---

## 📚 Advanced Features

### Dry Run Mode

Test operations without actual deletion:
1. Go to Settings (option `4`)
2. Enable "Dry Run Mode"
3. All operations will be simulated

### Logging

All operations are logged to:
- **Windows:** `%USERPROFILE%\.terminus\logs\`
- **Linux/macOS:** `~/.terminus/logs/`

View logs from main menu (option `5`)

### System Information

View detailed system info:
1. Go to Settings (option `4`)
2. Select "System Info" (option `5`)
3. View OS, memory, disk space, and privileges

---

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

**"Permission denied"**
- Windows: Run as Administrator
- Linux/macOS: Use `sudo`

**"Module not found"**
- Run the installer script again
- Or manually: `pip install psutil colorama`

**"Operation not permitted" (macOS)**
1. Go to System Preferences → Security & Privacy → Privacy
2. Select Full Disk Access
3. Add Terminal to allowed list

**"Gatekeeper blocking" (macOS)**
```bash
xattr -d com.apple.quarantine terminus.py
```

---

## ⚖️ Legal & Compliance

- **Corporate Environments:** Consult IT before use
- **Licensed Software:** Ensure compliance with licenses
- **Data Protection:** Follow local data protection regulations
- **Audit Trails:** All operations are logged for compliance

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **GNU General Public License v3.0**.  
See `LICENSE.txt` for details.

---

## ⭐ Support

- **🐛 Bug Reports:** [GitHub Issues](https://github.com/sarat1kyan/terminus/issues)
- **💡 Feature Requests:** [GitHub Issues](https://github.com/sarat1kyan/terminus/issues)
- **📖 Documentation:** [Project Wiki](https://github.com/sarat1kyan/terminus/wiki)
- **💬 Discussions:** [GitHub Discussions](https://github.com/sarat1kyan/terminus/discussions)

---

## 🙏 Acknowledgments

Built with ❤️ by **Mher Saratikyan | HEXESHELL**

Special thanks to all contributors and the open-source community.

---

<div align="center">

**⭐ If Terminus has helped you, please star the repository! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/sarat1kyan/Terminus?style=social)](https://github.com/sarat1kyan/Terminus/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/sarat1kyan/Terminus?style=social)](https://github.com/sarat1kyan/Terminus/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/sarat1kyan/Terminus?style=social)](https://github.com/sarat1kyan/Terminus/watchers)

---

### 🔗 Quick Links

[📥 **Download**](https://github.com/sarat1kyan/Terminus/archive/refs/heads/main.zip) • 
[📖 **Documentation**](https://github.com/sarat1kyan/Terminus/wiki) • 
[🐛 **Report Bug**](https://github.com/sarat1kyan/Terminus/issues) • 
[💡 **Request Feature**](https://github.com/sarat1kyan/Terminus/issues) • 
[💬 **Discussions**](https://github.com/sarat1kyan/Terminus/discussions)

---

```
When the going gets tough, the tough get Terminus.
```

**Version 5.0 ULTIMATE** - The most powerful system cleaner ever built.

</div>
