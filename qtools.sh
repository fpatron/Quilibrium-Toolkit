#!/bin/bash

# Script Name: Quilibrium Runner (qtools.sh)
# Author: vodhash
# Version: 1.0
# Description: Automates the execution of Quilibrium monitoring tasks by simplifying commands.

HOSTS_FILE="inventories/hosts.yml"
VAULT_FILE="vaults/vault.yml"

# Find dynamically available playbooks
declare -A command_paths
while IFS= read -r -d '' file; do
    playbook_path="${file#playbooks/}"
    filename=$(basename "$file")
    command_name="${filename%.*}"
    command_paths["$command_name"]="$playbook_path"
done < <(find playbooks -type f -name "*.yml" -print0)

# Check if command is valid
if [ $# -eq 0 ] || [ "$1" == "--help" ] || [ $# -lt 2 ] || [ -z "${command_paths[$1]}" ]; then
  echo "Quilibrium Runner"
  echo "------------------------"
  echo "This script simplifies the execution of Quilibrium monitoring tasks by automating the common command structure, adding basic checks for file existence, and providing detailed error messages."
  echo "https://github.com/fpatron/Quilibrium-Toolkit"
  echo ""
  echo "Usage:"
  echo "./qtools.sh <command> <host>"
  echo ""
  echo "Arguments:"
  echo "- <command>: The command to perform."
  echo "- <host>: The name of the target host, group, or 'all' to execute the playbook on."
  echo ""
  echo "**Supported commands:**"
  echo "  - get_node_info: Return information about the Quilibrium targets(s)"
  echo "  - get_node_reward: Get rewards from targets(s)"
  echo "  - start_node: Starts the Quilibrium targets(s)"
  echo "  - stop_node: Stops the Quilibrium targets(s)"
  echo "  - restart_node: Restarts the Quilibrium targets(s)"
  echo "  - backup_node: Backup Quilibrium configuration files"
  echo "  - install_node: Install a new Quilibrium node on the specified targets(s)"
  echo "  - upgrade_node: Upgrade Quilibrium node on the specified targets(s)"
  echo "  - setup_node: Configure sysctl and listen port on the specified targets(s)"
  echo "  - create_service: Install your Quilibrium node as a service"
  echo "  - fastsync_node: Sync your node with the latest snapshot"
  echo "  - reboot_node: Reboot the specified targets(s)"
  echo ""
  echo "  - install_watchdog: Monitor your node and get notify about its status (see readme for more details)"
  echo "  - start_watchdog: Start watchdog service"
  echo "  - stop_watchdog: Stop watchdog service"
  echo "  - restart_watchdog: Restart watchdog service"
  echo ""
  echo "Example:"
  echo "./qtools.sh start_node node01"
  echo ""
  echo "Requirements:"
  echo "- The script requires the following files to exist:"
  echo "    - inventories/hosts.yml: The Ansible hosts inventory file."
  echo "    - vaults/vault.yml: The Ansible Vault file containing sensitive credentials (optional)."
  echo "- The script assumes that the 'ansible' command is available in the system's PATH environment variable."
  echo ""
  exit 0
fi

# Check if hosts inventory file exists
if [ ! -f "$HOSTS_FILE" ]; then
  echo "Error: Hosts inventory file ($HOSTS_FILE) not found."
  echo "Create a hosts inventory file following Ansible conventions."
  exit 1
fi

# Check if Vault file exists
if [ ! -f "$VAULT_FILE" ]; then
  echo "Error: Vault file ($VAULT_FILE) not found."
  echo "Create a Vault file to store sensitive credentials."
  exit 1
fi

# Handle extra vars
extra_vars=""
for ((i=3; i<=$#; i++)); do
  option=${!i}
  if [ -n "$option" ]; then
    extra_vars="${extra_vars} -e ${option}"
  fi
done
extra_vars=$(echo "$extra_vars" | sed 's/^ *//; s/ *$//')

# Construct playbook full path
playbook_path="playbooks/${command_paths[$1]}"

# Execute playbook
ansible-playbook -i ${HOSTS_FILE} -e target=$2 -e @${VAULT_FILE} $extra_vars --ssh-common-args='-o StrictHostKeyChecking=no' --ask-vault-pass $playbook_path
