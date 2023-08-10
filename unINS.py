import os
import shutil
import winreg
import subprocess
import time

def search_program(program_name):
    # Search for the program's files and directories
    files_found = []
    dirs_found = []

    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if program_name.lower() in file.lower():
                files_found.append(os.path.join(root, file))
        for dir in dirs:
            if program_name.lower() in dir.lower():
                dirs_found.append(os.path.join(root, dir))

    # Search for the program's registry keys
    registry_keys = []
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software")
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            if program_name.lower() in subkey_name.lower():
                registry_keys.append(os.path.join('Software', subkey_name))
    except OSError:
        pass

    return files_found, dirs_found, registry_keys

def backup_files(files, backup_dir):
    # Create a backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Copy files to the backup directory
    for file in files:
        dest = os.path.join(backup_dir, os.path.basename(file))
        shutil.copy2(file, dest)

def backup_registry_keys(keys, backup_file):
    # Export the registry keys to a backup file
    with open(backup_file, 'w') as f:
        for key in keys:
            f.write(f'reg export "{key}" "{backup_file}"\n')

def uninstall_program(program_name, backup=True, silent=False):
    # Check if the program is installed
    installed = False
    try:
        process = subprocess.Popen(['wmic', 'product', 'get', 'name'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = process.communicate()
        if program_name in output:
            installed = True
    except Exception as e:
        print(f"An error occurred while checking if {program_name} is installed: {e}")

    if installed:
        # Create a backup if enabled
        if backup:
            backup_dir = f"{program_name}_backup"
            backup_file = f"{program_name}_registry_backup.reg"

            # Backup files
            files_found, dirs_found, registry_keys = search_program(program_name)
            backup_files(files_found + dirs_found, backup_dir)
            backup_registry_keys(registry_keys, backup_file)

        # Uninstall the program using the WMIC command
        print(f"Uninstalling {program_name}...")
        command = ['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall']
        if silent:
            command.append('/nointeractive')
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            _, error = process.communicate()
            if error:
                print(f"Error occurred while uninstalling {program_name}: {error}")
            else:
                print(f"{program_name} was successfully uninstalled.")
        except Exception as e:
            print(f"An error occurred while uninstalling {program_name}: {e}")
    else:
        print(f"{program_name} is not installed.")

def main():
    try:
        # Prompt the user to enter the program name
        program_name = input("Enter the program name to search and uninstall: ")

        # Search for the program
        print("Searching for the program...")
        files_found, dirs_found, registry_keys = search_program(program_name)

        # Display the search results
        if files_found or dirs_found or registry_keys:
            print("Program found.")
            print("Files found:")
            for file in files_found:
                print(file)
            print("Directories found:")
            for dir in dirs_found:
                print(dir)
            print("Registry keys found:")
            for key in registry_keys:
                print(key)

            # Prompt the user for further actions
            backup_option = input("Do you want to create a backup of the program files and registry keys? (y/n): ")
            if backup_option.lower() == 'y':
                backup_dir = f"{program_name}_backup"
                backup_files(files_found + dirs_found, backup_dir)
                backup_file = f"{program_name}_registry_backup.reg"
                backup_registry_keys(registry_keys, backup_file)
                print("Backup created.")

            uninstall_option = input("Do you want to uninstall the program? (y/n): ")
            if uninstall_option.lower() == 'y':
                silent_option = input("Do you want to perform a silent uninstallation? (y/n): ")
                if silent_option.lower() == 'y':
                    uninstall_program(program_name, backup=False, silent=True)
                else:
                    uninstall_program(program_name, backup=False)

            # Wait for a few seconds to allow changes to take effect
            time.sleep(3)

            # Search again to verify if the program is uninstalled
            print("Searching again to verify uninstallation...")
            search_program(program_name)
        else:
            print("Program not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
