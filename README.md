                                
              _____ _____ _____ 
      _ _ ___|     |   | |   __|
     | | |   |-   -| | | |__   |
     |___|_|_|_____|_|___|_____|
                                                         

# unINS
Unleash Python's power with this uninstaller script. Bid farewell to unwanted software as it explores your system, leaving no trace. Deep searches, registry detection, and 'wmic' magic remove programs.

WARNING: This script can potentially harm your system if used improperly. Only use it if you fully understand its functionality and are aware of the risks.

The "Uninstall Program Helper" script is a Python program designed to assist users in searching for, creating backups of, and potentially uninstalling software programs from a Windows system. The script provides a user-friendly interface for these tasks, allowing users to specify the program they want to target and offering options to back up relevant files and registry keys before proceeding with the uninstallation.

The script works by performing a comprehensive search throughout the system for files, directories, and registry keys associated with the specified program name. Once the search is complete, the script displays the search results, showing the paths of files, directories, and registry keys that match the program name.

Users are given the option to perform the following actions:

Backup Files and Registry Keys: Users can choose to create backups of the program's files and registry keys before proceeding with uninstallation. This backup can be valuable for restoring the program in case of any issues.

Uninstall the Program: Users can opt to uninstall the specified program. The script uses the Windows Management Instrumentation Command-line (WMIC) to initiate the uninstallation process. The script provides an option for silent uninstallation, which means the uninstallation will proceed without user interaction (use with caution).

WARNING: This script has the potential to impact your system, especially when performing uninstallations or modifying the Windows registry. It's essential to exercise caution and fully understand the consequences of using this script. Incorrect usage or uninstallation of critical software could cause system instability or data loss. Use this script only if you are confident in your understanding of its functionality and potential risks.

Before using this script, make sure you review the search results carefully, understand the implications of uninstalling the specified program, and consider creating backups of important data on your system. Always exercise caution and backup your important data before making any significant changes to your system. If you're unsure about using this script, seek assistance from a knowledgeable professional.

Remember, this script is intended for advanced users who have a good understanding of system operations and the potential consequences of uninstalling software and modifying the Windows registry. It's not suitable for casual users or those who are not familiar with the intricacies of software management on Windows systems.

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
