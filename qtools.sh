#!/bin/bash

# Script Name: Quilibrium Runner (qtools.sh)
# Author: vodhash
# Version: 1.0
# Description: Automates the execution of Quilibrium monitoring tasks by simplifying commands.

HOSTS_FILE="inventories/hosts.yml"
VAULT_FILE="vaults/vault.yml"

if [ $# -eq 0 ] || [ "$1" == "--help" ] || [ $# -ne 2 ] \
     || [ "$1" != "start_node" ] && [ "$1" != "stop_node" ] && [ "$1" != "restart_node" ] \
     && [ "$1" != "get_node_info" ] && [ "$1" != "backup_node" ] && [ "$1" != "install_node" ]\
     && [ "$1" != "reboot_node" ] && [ "$1" != "get_node_reward" ]; then
  echo "Quilibrium Runner"
  echo "------------------------"
  echo "This script simplifies the execution of Quilibrium monitoring tasks by automating the common command structure, adding basic checks for file existence, and providing detailed error messages."
  echo ""
  echo "Usage:"
  echo "./qtools.sh <action> <host>"
  echo ""
  echo "Arguments:"
  echo "- <action>: The action to perform."
  echo "- <host>: The name of the target host, group, or 'all' to execute the playbook on."
  echo ""
  echo "**Supported Actions:**"
  echo "  - get_node_info: Return information about the Quilibrium node(s)"
  echo "  - get_node_reward: Get rewards from node(s)"
  echo "  - start_node: Starts the Quilibrium node(s)"
  echo "  - stop_node: Stops the Quilibrium node(s)"
  echo "  - restart_node: Restarts the Quilibrium node(s)"
  echo "  - backup_node: Backup Quilibrium configuration files"
  echo "  - install_node: Install a new Quilibrium node on the specified node(s)"
  echo "  - reboot_node: Reboot the specified node(s)"
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

# Execute the Ansible playbook
ansible-playbook -i ${HOSTS_FILE} -e target=$2 -e @${VAULT_FILE} --ssh-common-args='-o StrictHostKeyChecking=no' --ask-vault-pass playbooks/$1.yml
