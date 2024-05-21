# Quilibrium tools

## Overview

This project provides tools for managing Quilibrium nodes (https://github.com/QuilibriumNetwork/ceremonyclient). It helps with basic actions and monitoring for multiple nodes.<br/>
These tools are built using Ansible https://github.com/ansible/ansible.<br/>

## Pre-requisites
1. Install ansible on your PC
```
apt install ansible
```
2. Clone this repository.

## Commands
```
./qtools.sh <target> <action>
```

### Targets
You define targets in your Ansible inventory file [inventories/hosts.yml]

### Actions

| Action | Description |
| ---   | --- |
install_node | Installs a new Quilibrium node on the specified target(s).
backup_node | Backs up Quilibrium configuration files to the ./backup folder locally.
get_node_info | Retrieves information about the Quilibrium node(s).
get_node_reward | Retrieves rewards about the Quilibrium node(s).
start_node | Starts the Quilibrium node(s)
stop_node | Stops the Quilibrium node(s)
restart_node | Restarts the Quilibrium node(s)
reboot_node | Reboot the specified node(s)

### Examples

To restart all your nodes
```
./qtools.sh restart_node all
```
To restart nodes from the "quilibrium" group:
```
./qtools.sh restart_node quilibrium
```
To restart a single node:
```
./qtools.sh restart_node node01
```

## Hosts

Quilibrium Tools require you to define your inventory in the [inventories/hosts.yml](inventories/hosts.yml) file.<br/>
Here's an example::<br/>

```
nodes:
  vars:
    ansible_user: <user_name>
    ansible_password: '{{ quilibrium_password }}'
  hosts:
    node01:
      ansible_host: 192.168.1.1
    node01:
      ansible_host: 192.168.1.2
    node03:
      ansible_host: 192.168.1.3
```
or [inventories/hosts.example.yml](inventories/hosts.example.yml)

* Replace <your_username> with your actual username<br/>
* You can define multiple groups besides "nodes" to organize your nodes for specific purposes.
* Refer to the Ansible documentation for more information on inventories: https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html

## Securing Passwords

To protect your node passwords, consider using Ansible Vault to encrypt sensitive data. Here's how:<br>

1. Create a vault file:
```
ansible-vault create vaults/vault.yml
```
2. Add your passwords to the vault using the edit command:
```
ansible-vault edit vaults/vault.yml
```
Inside the editor, add a key-value pair like this:
```
quilibrium_password: my secure password
```
3. Update your hosts.yml file to reference the password from the vault:
```
ansible_password: '{{ quilibrium_password }}'
```
4. To edit your vault file:
```
ansible-vault edit vaults/vault.yml
```
5. To view your vault file:
```
ansible-vault view vaults/vault.yml
```
Note: The vault may use vim or nano by default for editing.

