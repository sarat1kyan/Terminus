import os
import shutil
import winreg
import subprocess
import time
import datetime
import logging

logging.basicConfig(filename='app_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
def search_program(program_name, case_sensitive=False):
    # Search for the program's files and directories
    files_found = []
    dirs_found = []
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if (not case_sensitive and program_name.lower() in file.lower()) or (case_sensitive and program_name in file):
                files_found.append(os.path.join(root, file))
        for dir in dirs:
            if (not case_sensitive and program_name.lower() in dir.lower()) or (case_sensitive and program_name in dir):
                dirs_found.append(os.path.join(root, dir))
    registry_keys = []
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software")
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            if (not case_sensitive and program_name.lower() in subkey_name.lower()) or (case_sensitive and program_name in subkey_name):
                registry_keys.append(os.path.join('Software', subkey_name))
    except OSError as e:
        logging.error(f"Error while searching registry keys: {e}")
    return files_found, dirs_found, registry_keys
def backup_files(files, backup_dir):
    # Create a backup directory with a timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f"{backup_dir}_{timestamp}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    for file in files:
        dest = os.path.join(backup_dir, os.path.basename(file))
        shutil.copy2(file, dest)
    logging.info(f"Files backed up to {backup_dir}")
def backup_registry_keys(keys, backup_file):
    # Export each registry key to a separate backup file
    for i, key in enumerate(keys):
        key_backup_file = f"{backup_file}_key_{i}.reg"
        with open(key_backup_file, 'w') as f:
            f.write(f'reg export "{key}" "{key_backup_file}"')
        logging.info(f"Registry key '{key}' backed up to {key_backup_file}")
def uninstall_program(program_name, backup=True, silent=False):
    installed = False
    try:
        process = subprocess.Popen(['wmic', 'product', 'get', 'name'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = process.communicate()
        if program_name in output:
            installed = True
    except Exception as e:
        logging.error(f"Error while checking if {program_name} is installed: {e}")
    if installed:
        if backup:
            backup_dir = program_name
            backup_file = f"{program_name}_registry_backup"
            files_found, dirs_found, registry_keys = search_program(program_name)
            backup_files(files_found + dirs_found, backup_dir)
            backup_registry_keys(registry_keys, backup_file)
        logging.info(f"Uninstalling {program_name}...")
        command = ['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall']
        if silent:
            command.append('/nointeractive')
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            _, error = process.communicate()
            if error:
                logging.error(f"Error occurred while uninstalling {program_name}: {error}")
            else:
                logging.info(f"{program_name} was successfully uninstalled.")
        except Exception as e:
            logging.error(f"An error occurred while uninstalling {program_name}: {e}")
    else:
        logging.warning(f"{program_name} is not installed.")
def main():
    try:
        program_name = input("Enter the program name to search and uninstall: ")
        logging.info(f"Searching for {program_name}...")
        files_found, dirs_found, registry_keys = search_program(program_name)
        if files_found or dirs_found or registry_keys:
            logging.info("Program found.")
            logging.info("Files found:")
            for file in files_found:
                logging.info(file)
            logging.info("Directories found:")
            for dir in dirs_found:
                logging.info(dir)
            logging.info("Registry keys found:")
            for key in registry_keys:
                logging.info(key)
            backup_option = input("Do you want to create a backup of the program files and registry keys? (y/n): ")
            if backup_option.lower() == 'y':
                backup_files(files_found + dirs_found, program_name)
                backup_registry_keys(registry_keys, f"{program_name}_registry_backup")

            uninstall_option = input("Do you want to uninstall the program? (y/n): ")
            if uninstall_option.lower() == 'y':
                silent_option = input("Do you want to perform a silent uninstallation? (y/n): ")
                if silent_option.lower() == 'y':
                    uninstall_program(program_name, backup=False, silent=True)
                else:
                    uninstall_program(program_name, backup=False)
            time.sleep(3)
            logging.info("Searching again to verify uninstallation...")
            search_program(program_name)
        else:
            logging.warning("Program not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
if __name__ == "__main__":
    main()
