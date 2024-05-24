                                
              _____ _____ _____ 
      _ _ ___|     |   | |   __|
     | | |   |-   -| | | |__   |
     |___|_|_|_____|_|___|_____|
                                                         

# unINS 3.0
Unleash Python's power with this uninstaller script. Bid farewell to unwanted software as it explores your system, leaving no trace. Deep searches, registry detection, and 'wmic' magic remove programs.

# Windows Program Uninstaller

A Python script for uninstalling programs from a Windows system with advanced cleanup options.

## Overview

This script provides a command-line interface to uninstall programs from a Windows system. It offers both regular and advanced uninstallation modes to cater to different user needs.

### Features

- Uninstall programs using their uninstall strings obtained from the Windows Registry.
- Advanced mode performs additional cleanup tasks, including deleting registry keys, files, services, and tasks related to the specified program.
- Easy-to-use command-line interface with user prompts and error handling.
- Logging functionality to record activities, errors, and outcomes for troubleshooting.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sarat1kyan/unINS.git



   Install dependencies:

pip install -r requirements.txt
Download the Sysinternals Suite from Microsoft and extract psexec.exe to the same directory as the script.

Usage
Open Command Prompt or Terminal.

Navigate to the directory containing the script (unINS.py).

Run the script:

python unINS.py
Follow the on-screen prompts to enter the program name and choose the uninstallation mode (regular/advanced).

Confirm the uninstallation when prompted.

Example
To uninstall a program named "Example Program" in advanced mode:

Run the script and enter "Example Program" as the program name.
Choose "advanced" mode.
Follow the prompts to confirm the uninstallation and cleanup.
Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.

Disclaimer
This script modifies system settings and performs potentially irreversible actions. Use it at your own risk.
