#!/bin/bash

function search_program {
    program_name=$1
    case_sensitive=$2

    files_found=()
    dirs_found=()

    # Search for the program's files and directories
    while IFS= read -r -d '' file; do
        files_found+=("$file")
    done < <(find / -type f -iname "*$program_name*" -print0)

    while IFS= read -r -d '' dir; do
        dirs_found+=("$dir")
    done < <(find / -type d -iname "*$program_name*" -print0)

    # Search for the program's package
    package=$(dpkg -l | grep -i "$program_name" | awk '{print $2}')

    echo "${files_found[@]}" "${dirs_found[@]}" "$package"
}

function backup_files {
    files=("$@")
    backup_dir="backup_$(date +'%Y%m%d_%H%M%S')"

    # Create a backup directory
    mkdir "$backup_dir"

    # Copy files to the backup directory
    for file in "${files[@]}"; do
        dest="$backup_dir/$(basename "$file")"
        cp "$file" "$dest"
    done

    echo "Files backed up to $backup_dir"
}

function uninstall_program {
    program_name=$1
    backup=$2
    silent=$3

    # Check if the program is installed
    package=$(dpkg -l | grep -i "$program_name" | awk '{print $2}')
    if [ -n "$package" ]; then
        # Backup files if enabled
        if [ "$backup" = true ]; then
            files_found=($(search_program "$program_name" false | cut -d' ' -f1-))
            backup_files "${files_found[@]}"
        fi

        # Uninstall the program using apt
        echo "Uninstalling $program_name..."
        if [ "$silent" = true ]; then
            apt-get -y remove "$package"
        else
            apt-get remove "$package"
        fi

        echo "$program_name was successfully uninstalled."
    else
        echo "$program_name is not installed."
    fi
}

# Main script
echo "Enter the program name to search and uninstall: "
read -r program_name

# Search for the program
search_result=$(search_program "$program_name" false)
files_found=($(echo "$search_result" | cut -d' ' -f1-))
dirs_found=($(echo "$search_result" | cut -d' ' -f"${#files_found[@]}-" -))

# Display the search results
if [ ${#files_found[@]} -gt 0 ] || [ ${#dirs_found[@]} -gt 0 ]; then
    echo "Program found."
    echo "Files found:"
    printf "%s\n" "${files_found[@]}"
    echo "Directories found:"
    printf "%s\n" "${dirs_found[@]}"

    # Prompt the user for further actions
    echo "Do you want to create a backup of the program files? (y/n): "
    read -r backup_option
    if [ "$backup_option" = "y" ]; then
        backup_files "${files_found[@]}"
        echo "Backup created."
    fi

    echo "Do you want to uninstall the program? (y/n): "
    read -r uninstall_option
    if [ "$uninstall_option" = "y" ]; then
        echo "Do you want to perform a silent uninstallation? (y/n): "
        read -r silent_option
        if [ "$silent_option" = "y" ]; then
            uninstall_program "$program_name" true true
        else
            uninstall_program "$program_name" true false
        fi
    fi
else
    echo "Program not found."
fi
