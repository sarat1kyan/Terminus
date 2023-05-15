     █    ██  ███▄    █  ██▓ ███▄    █   ██████ 
     ██  ▓██▒ ██ ▀█   █ ▓██▒ ██ ▀█   █ ▒██    ▒ 
    ▓██  ▒██░▓██  ▀█ ██▒▒██▒▓██  ▀█ ██▒░ ▓██▄   
    ▓▓█  ░██░▓██▒  ▐▌██▒░██░▓██▒  ▐▌██▒  ▒   ██▒
    ▒▒█████▓ ▒██░   ▓██░░██░▒██░   ▓██░▒██████▒▒
    ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▓  ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
    ░░▒░ ░ ░ ░ ░░   ░ ▒░ ▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░
     ░░░ ░ ░    ░   ░ ░  ▒ ░   ░   ░ ░ ░  ░  ░  
       ░              ░  ░           ░       ░  
                                                

# unINS
Unleash Python's power with this uninstaller script. Bid farewell to unwanted software as it explores your system, leaving no trace. Deep searches, registry detection, and 'wmic' magic remove programs.

==================================================
unINS - README
==================================================

This Python script allows you to search for installed programs, including their files, directories, and registry keys, and uninstall them from your Windows system.

---------------------------------------------------------------------------
Script Usage
---------------------------------------------------------------------------

1. Make sure you have Python installed on your Windows system. If Python is not installed, visit https://www.python.org/downloads/ to download and install it.

2. Place the Python script in a directory of your choice.

3. Open a command prompt or terminal and navigate to the directory containing the Python script.

4. Execute the script by running the following command: `python unINS.py`

5. Follow the instructions provided by the script to search for programs and choose whether to create backups and perform the uninstallation.

6. When prompted, enter the name of the program you want to search for and uninstall. Make sure to provide the program name accurately.

7. Wait for the script to complete the uninstallation process. You will receive status updates in the command prompt or terminal.

---------------------------------------------------------------------------
What this script can do
---------------------------------------------------------------------------

- Search for installed programs: The script allows you to search for programs installed on your Windows system. It scans files, directories, and registry keys to find programs matching your search query.

- Display search results: After searching for programs, the script displays the found files, directories, and registry keys associated with the programs.

- Create backups: You have the option to create backups of program files and registry keys before performing uninstallation. Backups can help you restore the programs if needed.

- Uninstall programs: The script utilizes the `wmic` command-line tool to uninstall programs. It provides a simple and automated way to remove unwanted software from your system.

- Silent uninstallation: You can choose to perform a silent uninstallation, which eliminates any prompts or user intervention during the uninstallation process.

---------------------------------------------------------------------------
Dependencies
---------------------------------------------------------------------------

The script requires the following Python modules:

- `os`
- `shutil`
- `winreg`
- `subprocess`
- `time`

Ensure that these modules are available in your Python environment.

---------------------------------------------------------------------------
Note
---------------------------------------------------------------------------

- The script uses the `wmic` command-line tool to perform the uninstallation. Ensure that it is available on your Windows system.

- Take caution when uninstalling programs. Make sure to carefully review the programs listed and confirm your actions before proceeding.

- When prompted for the program name, provide the name of the program you want to search for and uninstall accurately.

- The script provides the option to create backups of program files and registry keys. It is recommended to create backups before uninstalling programs.

- The script may require administrative privileges to perform certain operations. Run the script with administrative rights for a smoother experience.

- For any issues or questions, please reach out for support.

---------------------------------------------------------------------------
Disclaimer: Important Notice
---------------------------------------------------------------------------

Please note that this script is a powerful system tool that can have a significant impact on your computer. While it is designed to safely uninstall programs, it's crucial to exercise caution and understand the potential risks involved.

- Data Loss: Incorrect usage of the script can result in unintended deletion or modification of files and directories. Ensure you have appropriate backups in place before proceeding.

- Registry Modifications: The script interacts with the Windows Registry to locate and remove program entries. Inaccurate modification of registry keys can cause system instability or affect the functioning of other software.

- System Integrity: It's essential to verify the accuracy of program detection and confirmation before proceeding with uninstallation. Mistakenly removing critical system components can lead to system malfunction.

- User Responsibility: By using this script, you acknowledge that you are solely responsible for any consequences that may arise. Exercise caution, double-check your inputs, and review the code before running it.

- Usage Warning: We strongly recommend testing the script on non-production or disposable environments before running it on critical systems.

The script is provided as-is without any warranties or guarantees. Use it at your own risk. If you are uncertain or uncomfortable with the process, seek assistance from a knowledgeable professional.
