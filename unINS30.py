import subprocess
import os
import sys
import winreg as reg
import shutil
import ctypes
import logging
import unittest

# Configure logging
logging.basicConfig(filename='uninstall_program.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def is_admin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        logging.info(f"Is admin: {is_admin}")
        return is_admin
    except Exception as e:
        logging.error(f"Error checking admin privileges: {str(e)}")
        return False

def handle_error(error_message):
    print(error_message)
    logging.error(error_message)

def find_program(program_name):
    installed_programs = []

    def search_registry(hkey, key):
        try:
            with reg.OpenKey(hkey, key) as sub_key:
                for i in range(0, reg.QueryInfoKey(sub_key)[0]):
                    sub_key_name = reg.EnumKey(sub_key, i)
                    sub_key_path = os.path.join(key, sub_key_name)
                    try:
                        with reg.OpenKey(hkey, sub_key_path) as program_key:
                            display_name = reg.QueryValueEx(program_key, "DisplayName")[0]
                            if program_name.lower() in display_name.lower():
                                installed_programs.append((display_name, sub_key_path))
                    except FileNotFoundError:
                        continue
                    except Exception as e:
                        print(f"Error accessing registry key: {str(e)}")
        except Exception as e:
            print(f"Error accessing registry key: {str(e)}")

    search_registry(reg.HKEY_LOCAL_MACHINE, "")
    search_registry(reg.HKEY_CURRENT_USER, "")

    return installed_programs

#def find_program(program_name):
#   uninstall_keys = [
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
#        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # Additional 32-bit software path
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\Packages",  # Windows packages
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\PackagesPending",  # Pending Windows packages
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\ComponentDetect",  # Component detection
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products",  # Installed products
#        r"SOFTWARE\Classes\Installer\Products",  # Installed products from Installer
#        r"SOFTWARE\Classes\Installer\Features",  # Features from Installer
#        r"SOFTWARE\Classes\Installer\UpgradeCodes",  # Upgrade codes from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\WixBundleInstalled",  # WiX bundle installed
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{6E4D73D3-FAEB-4D9E-A116-236693F6D8B9}_is1",  # Example: specific program
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Components",  # Components from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\Folders",  # Folders from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\Assemblies",  # Assemblies from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\Win32Assemblies",  # Win32 Assemblies from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData",  # User data from Installer
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft SQL Server",  # Microsoft SQL Server
#        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Visual Studio",  # Microsoft Visual Studio
#        # Add more paths to check as needed
#    ]
#    installed_programs = []
#    
#    def search_registry(hkey, base_key):
#        with reg.OpenKey(hkey, base_key) as key:
#            for i in range(0, reg.QueryInfoKey(key)[0]):
#                sub_key_name = reg.EnumKey(key, i)
#                sub_key_path = os.path.join(base_key, sub_key_name)
#                with reg.OpenKey(hkey, sub_key_path) as sub_key:
#                    try:
#                        display_name = reg.QueryValueEx(sub_key, "DisplayName")[0]
#                        if program_name.lower() in display_name.lower():
#                            installed_programs.append((display_name, sub_key_path))
#                    except FileNotFoundError:
#                        continue
#    
#    for uninstall_key in uninstall_keys:
#        search_registry(reg.HKEY_LOCAL_MACHINE, uninstall_key)
#        search_registry(reg.HKEY_CURRENT_USER, uninstall_key)
#    
#    return installed_programs


def uninstall_program(program_name):
    try:
        programs = find_program(program_name)
        if not programs:
            handle_error(f"No program found with the name '{program_name}'")
            return

        for i, (name, path) in enumerate(programs):
            print(f"{i + 1}: {name}")

        try:
            choice = int(input("Choose the number of the program you want to uninstall: ")) - 1
            chosen_program = programs[choice]
        except (IndexError, ValueError):
            handle_error("Invalid choice.")
            return

        print(f"You have chosen to uninstall: {chosen_program[0]}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Uninstallation canceled.")
            return

        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, chosen_program[1]) as sub_key:
            uninstall_string = reg.QueryValueEx(sub_key, "UninstallString")[0]

        subprocess.run(uninstall_string, shell=True)
        logging.info(f"Uninstalled program: {chosen_program[0]}")
        print("Uninstallation completed.")

    except Exception as e:
        handle_error(f"Error during uninstallation: {str(e)}")

def advanced_uninstall_program(program_name):
    try:
        programs = find_program(program_name)
        if not programs:
            handle_error(f"No program found with the name '{program_name}'")
            return

        for i, (name, path) in enumerate(programs):
            print(f"{i + 1}: {name}")

        try:
            choice = int(input("Choose the number of the program you want to uninstall: ")) - 1
            chosen_program = programs[choice]
        except (IndexError, ValueError):
            handle_error("Invalid choice.")
            return

        print(f"You have chosen to uninstall: {chosen_program[0]}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Advanced uninstallation canceled.")
            return

        # Uninstall the program using its uninstall string
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, chosen_program[1]) as sub_key:
            uninstall_string = reg.QueryValueEx(sub_key, "UninstallString")[0]
        subprocess.run(uninstall_string, shell=True)

        # Advanced: Delete registry keys, files, services, and tasks
        delete_registry_keys(program_name)
        delete_related_files(program_name)
        delete_services_and_tasks(program_name)

        logging.info(f"Advanced uninstallation completed for program: {chosen_program[0]}")
        print("Advanced uninstallation completed.")

    except Exception as e:
        handle_error(f"Error during advanced uninstallation: {str(e)}")

def delete_registry_keys(program_name):
    print("Deleting registry keys...")
    
    def delete_keys(hkey, base_key):
        try:
            with reg.OpenKey(hkey, base_key) as key:
                for i in range(0, reg.QueryInfoKey(key)[0]):
                    sub_key_name = reg.EnumKey(key, i)
                    sub_key_path = os.path.join(base_key, sub_key_name)
                    with reg.OpenKey(hkey, sub_key_path) as sub_key:
                        try:
                            display_name = reg.QueryValueEx(sub_key, "DisplayName")[0]
                            if program_name.lower() in display_name.lower():
                                reg.DeleteKey(hkey, sub_key_path)
                        except FileNotFoundError:
                            continue
        except FileNotFoundError:
            print("Registry key not found.")
        except PermissionError:
            print("Permission denied. Please run the script as an administrator.")
    
    uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    delete_keys(reg.HKEY_LOCAL_MACHINE, uninstall_key)
    delete_keys(reg.HKEY_CURRENT_USER, uninstall_key)
    
    # Additional registry paths to search for remnants
    additional_paths = [
        r"SOFTWARE",
        r"SOFTWARE\Wow6432Node",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
    ]
    
    for base_key in additional_paths:
        delete_keys(reg.HKEY_LOCAL_MACHINE, base_key)
        delete_keys(reg.HKEY_CURRENT_USER, base_key)

def find_related_files(program_name):
    drives = ["{}:\\".format(d) for d in range(65, 91) if os.path.exists("{}:\\".format(chr(d)))]
    related_files = []

    def search_drive(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if program_name.lower() in file.lower():
                    related_files.append(os.path.join(root, file))

    for drive in drives:
        search_drive(drive)

    return related_files

def delete_services_and_tasks(program_name):
    print("Deleting related services and tasks...")
    
    try:
        service_query = subprocess.run(['sc', 'query', 'type=', 'service', 'state=', 'all'], capture_output=True, text=True)
        services = service_query.stdout.splitlines()
        for line in services:
            if program_name.lower() in line.lower():
                service_name = line.split()[1]
                subprocess.run(['sc', 'delete', service_name], shell=True)
    except Exception as e:
        print(f"Error deleting services: {e}")

    try:
        task_query = subprocess.run(['schtasks', '/query', '/fo', 'list', '/v'], capture_output=True, text=True)
        tasks = task_query.stdout.splitlines()
        task_name = None
        for line in tasks:
            if "TaskName:" in line:
                task_name = line.split(":")[1].strip()
            if program_name.lower() in line.lower() and task_name:
                subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], shell=True)
    except Exception as e:
        print(f"Error deleting tasks: {e}")


def main():
    try:
        if not is_admin():
            handle_error("Please run this script as an administrator.")
            return

        program_name = input("Enter the program name you want to uninstall: ").strip()
        if not program_name:
            handle_error("Program name cannot be empty.")
            return

        mode = input("Choose uninstallation mode (regular/advanced): ").strip().lower()
        if mode not in ["regular", "advanced"]:
            handle_error("Invalid mode selected.")
            return

        if mode == "regular":
            uninstall_program(program_name)
        elif mode == "advanced":
            advanced_uninstall_program(program_name)

    except Exception as e:
        handle_error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
