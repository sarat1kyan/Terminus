# Terminus Makefile
# For easy installation on Unix-like systems (Linux/macOS)

PYTHON := python3
PIP := pip3
SHELL := /bin/bash
PREFIX := /usr/local
INSTALL_DIR := $(PREFIX)/bin
CONFIG_DIR := $(HOME)/.terminus

# Detect OS
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    OS_NAME := Linux
endif
ifeq ($(UNAME_S),Darwin)
    OS_NAME := macOS
endif

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

.PHONY: all install uninstall clean test help check-deps dev-install

# Default target
all: check-deps install

help:
	@echo "Terminus Installation Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install    - Install Terminus and dependencies"
	@echo "  make uninstall  - Remove Terminus installation"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean temporary files"
	@echo "  make dev-install- Install with development dependencies"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Install locations:"
	@echo "  Binaries: $(INSTALL_DIR)"
	@echo "  Config:   $(CONFIG_DIR)"

check-deps:
	@echo -e "$(BLUE)Checking dependencies...$(NC)"
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo -e "$(RED)Python 3 is required but not installed.$(NC)" >&2; exit 1; }
	@$(PYTHON) -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" || { echo -e "$(RED)Python 3.10+ is required$(NC)"; exit 1; }
	@command -v $(PIP) >/dev/null 2>&1 || { echo -e "$(RED)pip3 is required but not installed.$(NC)" >&2; exit 1; }
	@echo -e "$(GREEN)✓ Dependencies OK$(NC)"

install: check-deps
	@echo -e "$(BLUE)Installing Terminus...$(NC)"
	
	# Create directories
	@mkdir -p $(CONFIG_DIR)/logs
	@echo -e "$(GREEN)✓ Created config directory$(NC)"
	
	# Install Python dependencies
	@echo -e "$(YELLOW)Installing Python packages...$(NC)"
	@$(PIP) install --user psutil colorama
	
	# Make scripts executable
	@chmod +x terminus.sh terminus.py
	@echo -e "$(GREEN)✓ Made scripts executable$(NC)"
	
	# Install to system (optional, requires sudo)
	@echo ""
	@echo -e "$(YELLOW)To install system-wide (optional):$(NC)"
	@echo "  sudo make system-install"
	@echo ""
	@echo -e "$(GREEN)Installation complete!$(NC)"
	@echo ""
	@echo "Run Terminus with:"
	@echo "  ./terminus.sh"
	@echo "  or"
	@echo "  python3 terminus.py"

system-install: install
	@echo -e "$(BLUE)Installing system-wide...$(NC)"
	@echo "This requires sudo privileges."
	
	# Copy files to system directories
	@sudo cp terminus.py $(INSTALL_DIR)/terminus
	@sudo chmod +x $(INSTALL_DIR)/terminus
	
	# Create wrapper script
	@echo '#!/bin/bash' | sudo tee $(INSTALL_DIR)/terminus-run >/dev/null
	@echo 'cd $$(dirname $$(readlink -f $$0))' | sudo tee -a $(INSTALL_DIR)/terminus-run >/dev/null
	@echo 'exec python3 terminus "$@"' | sudo tee -a $(INSTALL_DIR)/terminus-run >/dev/null
	@sudo chmod +x $(INSTALL_DIR)/terminus-run
	
	@echo -e "$(GREEN)✓ Installed to $(INSTALL_DIR)$(NC)"
	@echo ""
	@echo "You can now run Terminus from anywhere with:"
	@echo "  terminus"

dev-install: check-deps
	@echo -e "$(BLUE)Installing development dependencies...$(NC)"
	@$(PIP) install --user psutil colorama pytest pytest-cov black flake8 mypy
	@echo -e "$(GREEN)✓ Development dependencies installed$(NC)"

test:
	@echo -e "$(BLUE)Running tests...$(NC)"
	@if [ -f test_terminus.py ]; then \
		$(PYTHON) -m pytest test_terminus.py -v; \
	else \
		echo -e "$(YELLOW)No tests found$(NC)"; \
	fi

clean:
	@echo -e "$(BLUE)Cleaning up...$(NC)"
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo -e "$(GREEN)✓ Cleanup complete$(NC)"

uninstall:
	@echo -e "$(BLUE)Uninstalling Terminus...$(NC)"
	
	# Remove system files if they exist
	@if [ -f $(INSTALL_DIR)/terminus ]; then \
		echo "Removing system installation (requires sudo)..."; \
		sudo rm -f $(INSTALL_DIR)/terminus $(INSTALL_DIR)/terminus-run; \
	fi
	
	# Ask about config directory
	@echo ""
	@echo -e "$(YELLOW)Remove configuration and logs from $(CONFIG_DIR)? [y/N]$(NC)"
	@read -r response; \
	if [ "$$response" = "y" ] || [ "$$response" = "Y" ]; then \
		rm -rf $(CONFIG_DIR); \
		echo -e "$(GREEN)✓ Configuration removed$(NC)"; \
	else \
		echo "Configuration preserved"; \
	fi
	
	@echo -e "$(GREEN)✓ Uninstall complete$(NC)"

# Create distribution package
dist: clean
	@echo -e "$(BLUE)Creating distribution package...$(NC)"
	@mkdir -p dist
	@tar -czf dist/terminus-$(shell date +%Y%m%d).tar.gz \
		--exclude=dist \
		--exclude=.git \
		--exclude=__pycache__ \
		--exclude=*.pyc \
		.
	@echo -e "$(GREEN)✓ Package created in dist/$(NC)"

.DEFAULT_GOAL := help