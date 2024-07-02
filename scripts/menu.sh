#!/bin/bash

# Function to display menu with selected option in coulour
show_menu() {
    clear
    echo "QuilibriumToolKit Menu"
    echo "Choose an Option with UP/DOWN key and press ENTER :"
    for i in "${!options[@]}"; do
        if [ $i -eq $selected ]; then
            # Display selected option  with a blue background and white text
            echo -e "\033[44;97m> ${options[$i]}\033[0m"
        else
            echo "  ${options[$i]}"
        fi
    done
}

# Function to display host menu
show_hosts_menu() {
    clear
    echo "Choose the Host:"
    for i in "${!hosts[@]}"; do
        if [ $i -eq $selected_host ]; then
            # Display selected option  with a blue background and white text
            echo -e "\033[44;97m> ${hosts[$i]}\033[0m"
        else
            echo "  ${hosts[$i]}"
        fi
    done
}

# Function to load name hosts from inventories/hosts.yml
load_hosts() {
    yaml_file="inventories/hosts.yml"
    hosts=('all')
    
    # Read the file and extract the hosts names
    while IFS= read -r line; do
        if [[ $line == *"ansible_host:"* ]]; then
            # Store the name of the previous line
            host_name=$(echo "$prev_line" | awk -F: '{print $1}' | xargs)
            hosts+=("$host_name")
        fi
    prev_line="$line"
    done < "$yaml_file"
}

# Menu options Initialisation
options=("upgrade_node" "get_node_info" "get_node_reward" "start_node" "stop_node" "restart_node" 
         "backup_node" "restore_node" "install_node" "setup_node" 
         "create_service" "reboot_node" "install_grafana" "install_watchdog" 
         "start_watchdog" "stop_watchdog" "restart_watchdog" "Quit")
selected=0

# Loading hosts
load_hosts
selected_host=0

# Display initial menu
show_menu

# Reading user input
while true; do
    read -rsn1 input
    case "$input" in
        $'\x1B') 
            read -rsn2 -t 0.1 input
            if [ "$input" == "[A" ]; then
                ((selected--))
                [ $selected -lt 0 ] && selected=$((${#options[@]} - 1))
            elif [ "$input" == "[B" ]; then
                ((selected++))
                [ $selected -ge ${#options[@]} ] && selected=0
            fi
            show_menu
            ;;
        '') # ENTER Key
            case "${options[$selected]}" in
                "Quit")
                    clear
                    exit
                    ;;
                *)
                    while true; do
                        show_hosts_menu
                        read -rsn1 input
                        case "$input" in
                            $'\x1B') 
                                read -rsn2 -t 0.1 input
                                if [ "$input" == "[A" ]; then
                                    ((selected_host--))
                                    [ $selected_host -lt 0 ] && selected_host=$((${#hosts[@]} - 1))
                                elif [ "$input" == "[B" ]; then
                                    ((selected_host++))
                                    [ $selected_host -ge ${#hosts[@]} ] && selected_host=0
                                fi
                                show_hosts_menu
                                ;;
                            '') 
                                clear
                                command="./qtools.sh ${options[$selected]} ${hosts[$selected_host]}"
                                echo "Exécute command : $command"
                                eval "$command"
                                read -p "press one key to display main menu..."
                                show_menu
                                break
                                ;;
                        esac
                    done
                    ;;
            esac
            show_menu
            ;;
    esac
done
