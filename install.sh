#!/bin/bash
#
# Terminus Installation Script for Linux/macOS
# Automatically installs dependencies and sets up Terminus
#

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${CYAN}${BOLD}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗     ║"
echo "║     ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║     ║"
echo "║        ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║     ║"
echo "║        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║     ║"
echo "║        ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║     ║"
echo "║        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝     ║"
echo "║                                                            ║"
echo "║           Installation Script v5.0 ULTIMATE                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    if command -v lsb_release &> /dev/null; then
        DISTRO=$(lsb_release -si)
        DISTRO_VERSION=$(lsb_release -sr)
        echo -e "${GREEN}✓ Detected OS: ${BOLD}Linux ($DISTRO $DISTRO_VERSION)${NC}\n"
    else
        echo -e "${GREEN}✓ Detected OS: ${BOLD}Linux${NC}\n"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    MACOS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "Unknown")
    echo -e "${GREEN}✓ Detected OS: ${BOLD}macOS $MACOS_VERSION${NC}\n"
else
    echo -e "${RED}✗ Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python is not installed!${NC}"
    echo -e "\n${YELLOW}Please install Python 3.10 or higher:${NC}"
    if [[ "$OS" == "linux" ]]; then
        echo "  sudo apt install python3 python3-pip    # Debian/Ubuntu"
        echo "  sudo yum install python3 python3-pip    # RHEL/CentOS/Fedora"
        echo "  sudo pacman -S python python-pip        # Arch Linux"
        echo "  sudo zypper install python3 python3-pip # openSUSE"
    elif [[ "$OS" == "macos" ]]; then
        echo "  brew install python@3.11"
        echo "  Or download from: https://www.python.org/downloads/"
    fi
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}✗ Python 3.10 or higher is required!${NC}"
    echo -e "  Your version: ${RED}$PYTHON_VERSION${NC}"
    echo -e "  Required: ${GREEN}$REQUIRED_VERSION+${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}\n"

# Check pip
echo -e "${YELLOW}Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${YELLOW}⚠ pip not found, installing...${NC}"
    $PYTHON_CMD -m ensurepip --upgrade || {
        echo -e "${RED}✗ Failed to install pip${NC}"
        exit 1
    }
    PIP_CMD="$PYTHON_CMD -m pip"
fi
echo -e "${GREEN}✓ pip found${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}\n"

REQUIRED_PACKAGES=("psutil" "colorama")
INSTALLED=0
FAILED=0

for package in "${REQUIRED_PACKAGES[@]}"; do
    echo -n "  Installing $package... "
    if $PIP_CMD install --upgrade --quiet "$package" 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((INSTALLED++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED++))
    fi
done

echo ""
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed to install some packages${NC}"
    echo -e "${YELLOW}Try installing manually:${NC}"
    echo "  $PIP_CMD install psutil colorama"
    exit 1
fi

echo -e "${GREEN}✓ All dependencies installed successfully${NC}\n"

# Create directories
echo -e "${YELLOW}Creating Terminus directories...${NC}"
TERMINUS_DIR="$HOME/.terminus"
LOGS_DIR="$TERMINUS_DIR/logs"

mkdir -p "$TERMINUS_DIR" "$LOGS_DIR"
echo -e "${GREEN}✓ Created $TERMINUS_DIR${NC}\n"

# Make scripts executable
echo -e "${YELLOW}Setting up launcher scripts...${NC}"
if [ -f "terminus.sh" ]; then
    chmod +x terminus.sh
    echo -e "${GREEN}✓ Made terminus.sh executable${NC}"
fi
if [ -f "terminus.py" ]; then
    chmod +x terminus.py
    echo -e "${GREEN}✓ Made terminus.py executable${NC}"
fi
echo ""

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
if [ ! -f "terminus.py" ]; then
    echo -e "${RED}✗ terminus.py not found!${NC}"
    echo "Make sure you're running this script from the Terminus directory."
    exit 1
fi

# Test imports
if $PYTHON_CMD -c "import psutil, colorama" 2>/dev/null; then
    echo -e "${GREEN}✓ All modules imported successfully${NC}\n"
else
    echo -e "${RED}✗ Module import failed${NC}\n"
    exit 1
fi

# Success message
echo -e "${GREEN}${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║                                                            ║${NC}"
echo -e "${GREEN}${BOLD}║           Installation Complete! ✓                        ║${NC}"
echo -e "${GREEN}${BOLD}║                                                            ║${NC}"
echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${CYAN}${BOLD}To run Terminus:${NC}"
echo -e "  ${WHITE}./terminus.sh${NC}        # Recommended (handles dependencies)"
echo -e "  ${WHITE}$PYTHON_CMD terminus.py${NC}  # Direct execution\n"

if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠ Note: Some features require root privileges${NC}"
    echo -e "  Run with: ${WHITE}sudo ./terminus.sh${NC}\n"
fi

echo -e "${YELLOW}${BOLD}First time usage tips:${NC}"
echo -e "  1. Start with 'Scan System Software' to see what's installed"
echo -e "  2. Enable 'Dry Run Mode' in Settings to test safely"
echo -e "  3. Always backup important data before removing software"
echo -e "  4. Test in a virtual machine first!\n"

echo -e "${RED}${BOLD}⚠ WARNING:${NC} ${RED}This tool can permanently remove software and files!${NC}\n"

