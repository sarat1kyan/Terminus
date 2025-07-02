#!/bin/bash
#
# Terminus - System Software Manager
# Linux/macOS Launcher Script
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${CYAN}"
echo "========================================"
echo "   Terminus - System Software Manager"
echo "        Linux/macOS Launcher"
echo "========================================"
echo -e "${NC}"

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
    echo -e "${GREEN}Detected OS: Linux ($DISTRO)${NC}"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo -e "${GREEN}Detected OS: macOS$(sw_vers -productVersion 2>/dev/null)${NC}"
else
    echo -e "${RED}Warning: Unknown operating system${NC}"
fi

echo

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python is not installed!${NC}"
    echo "Please install Python 3.10 or higher."
    
    if [[ "$OS" == "linux" ]]; then
        echo -e "\nInstall with:"
        echo "  sudo apt install python3 python3-pip    # Debian/Ubuntu"
        echo "  sudo yum install python3 python3-pip    # RHEL/CentOS"
        echo "  sudo pacman -S python python-pip        # Arch Linux"
    elif [[ "$OS" == "macos" ]]; then
        echo -e "\nInstall with:"
        echo "  brew install python@3.11"
    fi
    
    exit 1
fi

# Get Python version
python_version=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

echo -e "Python version: ${BLUE}$python_version${NC}"

# Compare versions
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo -e "${RED}Error: Python 3.10 or higher is required!${NC}"
    echo "Your version: $python_version"
    echo "Required version: $required_version"
    exit 1
fi

echo

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${GREEN}✓ Running as root${NC}"
else
    echo -e "${YELLOW}⚠ Warning: Not running as root${NC}"
    echo
    echo "Some features will be limited without root privileges:"
    echo "  - Cannot remove system packages"
    echo "  - Cannot modify system files"
    echo "  - Cannot stop system services"
    echo
    echo "To run with root privileges:"
    echo -e "  ${WHITE}sudo ./terminus.sh${NC}"
    echo
    read -p "Continue with limited privileges? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo

# Function to check if a Python module is installed
check_module() {
    $PYTHON_CMD -c "import $1" 2>/dev/null
    return $?
}

# Check dependencies
echo "Checking dependencies..."
missing_deps=()

if ! check_module "psutil"; then
    missing_deps+=("psutil")
fi

if ! check_module "colorama"; then
    missing_deps+=("colorama")
fi

# Install missing dependencies
if [ ${#missing_deps[@]} -ne 0 ]; then
    echo -e "${YELLOW}Missing dependencies: ${missing_deps[*]}${NC}"
    echo "Installing required packages..."
    echo
    
    # Determine pip command
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        echo -e "${RED}Error: pip is not installed!${NC}"
        
        if [[ "$OS" == "linux" ]]; then
            echo -e "\nInstall pip with:"
            echo "  sudo apt install python3-pip    # Debian/Ubuntu"
            echo "  sudo yum install python3-pip    # RHEL/CentOS"
            echo "  sudo pacman -S python-pip       # Arch Linux"
        elif [[ "$OS" == "macos" ]]; then
            echo -e "\nPip should be included with Python from Homebrew"
            echo "Try: python3 -m ensurepip"
        fi
        
        exit 1
    fi
    
    # Install with appropriate privileges
    if [ "$EUID" -eq 0 ]; then
        $PIP_CMD install ${missing_deps[*]}
    else
        echo -e "${YELLOW}Installing to user directory...${NC}"
        $PIP_CMD install --user ${missing_deps[*]}
    fi
    
    # Verify installation
    echo
    echo "Verifying installation..."
    for dep in "${missing_deps[@]}"; do
        if check_module "$dep"; then
            echo -e "${GREEN}✓ $dep installed successfully${NC}"
        else
            echo -e "${RED}✗ Failed to install $dep${NC}"
            exit 1
        fi
    done
else
    echo -e "${GREEN}✓ All dependencies are installed${NC}"
fi

echo

# Create necessary directories
TERMINUS_DIR="$HOME/.terminus"
if [ ! -d "$TERMINUS_DIR" ]; then
    echo "Creating Terminus directory..."
    mkdir -p "$TERMINUS_DIR/logs"
    echo -e "${GREEN}✓ Created $TERMINUS_DIR${NC}"
fi

# Check if terminus.py exists
if [ ! -f "terminus.py" ]; then
    echo -e "${RED}Error: terminus.py not found in current directory!${NC}"
    echo "Make sure you're running this script from the Terminus directory."
    exit 1
fi

echo

# Set terminal to UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Run Terminus
echo -e "${GREEN}Starting Terminus...${NC}"
echo -e "${CYAN}════════════════════════════════════════${NC}"
echo

# Execute with all passed arguments
$PYTHON_CMD terminus.py "$@"

# Capture exit code
exit_code=$?

# Check exit status
echo
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}Terminus exited successfully${NC}"
else
    echo -e "${RED}Terminus exited with error code: $exit_code${NC}"
    echo "Check logs in: $TERMINUS_DIR/logs/"
fi

# End of script