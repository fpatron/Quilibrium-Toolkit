# Quilibrium Tools: Manage Your Nodes with Ease

This project provides a comprehensive toolkit for simplifying the management of your Quilibrium nodes.<br/>
With these tools, you can perform essential actions and monitor multiple nodes effortlessly, saving you valuable time and ensuring smooth operation.<br/>
https://github.com/QuilibriumNetwork/ceremonyclient

## Overview

* **Centralized Management:** manage multiple Quilibrium nodes from a single location, eliminating the need to interact with each node individually.
* **Simplified Actions:** perform common tasks like installation, backup, retrieval of information and rewards, starting/stopping/rebooting nodes with a single command.
* **Flexibility:** group your nodes for targeted management or manage them all at once.
* **Security:** leverage Ansible's robust features to manage passwords securely using Ansible Vault (explained in detail later).
* **Built with Ansible:** This toolkit utilizes the power of Ansible, a popular open-source automation tool, for efficient node management (https://github.com/ansible/ansible).


## Getting Started
1. **Install Ansible**
```
apt install ansible
```
2. **Install Python 3**
```
apt install python3
```
3. **Clone this repository:** use git to clone this repository onto your local system.

## Commands

The tools are provided as a script named ```qtools.sh```. To use it, follow this syntax:

```
./qtools.sh <action> <target>
```

## Explanation

* <target>: This specifies the node(s) you want to target. It can be:
  * ```all```: Applies the action to all nodes defined in your inventory file.
  * A group name defined in your inventory (e.g., quilibrium).
  * The hostname of a specific node (e.g., node01).
* <action>: This defines the operation you want to perform on the target node(s). Available actions include:

| Action | Description |
| ---   | --- |
install_node | Installs a new Quilibrium node on the specified target(s).
setup_node | Configure sysctl and listen port (config.yml) on the specified node(s).
fastsync_node | Sync your node with the latest snapshot. If you are having difficulties with synchronization, you can use this task to install the latest snapshot store folder on your node.
create_service | Install your Quilibrium node as a service on the specified target(s) (see §Node commands).
backup_node | Creates a backup of Quilibrium configuration files on the target node(s) and saves them locally in the ```./backup``` folder.
get_node_info | Retrieves information about the Quilibrium node(s), such as its current max_frame, peer id...
get_node_reward | Fetches information about the rewards earned by the Quilibrium node(s).
start_node | Starts the Quilibrium node(s) on the target machine(s).
stop_node | Stops the Quilibrium node(s) running on the target machine(s).
restart_node | Restarts the Quilibrium node(s) on the target machine(s).
reboot_node | Reboots the entire node machine(s).
install_watchdog | Monitor your node and get notify about its status (see readme for more details)"
start_watchdog | Start watchdog service"
stop_watchdog | Stop watchdog service"
restart_watchdog | Restart watchdog service"


### Installing a Quilibrium node ```install_node```

The install_node action automates the process of setting up a new Quilibrium node on your target machine(s). Here's a detailed breakdown of what it does:

#### Installation directory
* By default, Quilibrium will be installed in the following directory:
```
/home/<your user>/quilibrium
```

#### Additional packages
* The script automatically installs any necessary additional packages required for Quilibrium to run correctly.

#### System configuration updates:
* The script modifies the system configuration file ```/etc/sysctl.conf``` to include the following parameters:
```
net.core.rmem_max=7500000
net.core.wmem_max=7500000
```
These parameters adjust the network buffer sizes to potentially improve Quilibrium's performance.

#### Quilibrium configuration
* The script set up the Quilibrium configuration file (```node/.config/config.yml```). It sets the following parameters within the configuration file:
```
statsMultiaddr: "/dns/stats.quilibrium.com/tcp/443"'
listenGrpcMultiaddr: /ip4/127.0.0.1/tcp/8337
listenRESTMultiaddr: /ip4/127.0.0.1/tcp/8338
```
* statsMultiaddr: this parameter defines the address where the node will send statistics.
* listenGrpcMultiaddr and listenRESTMultiaddr: these parameters specify the IP addresses and ports on which the node listens for incoming GRPC and REST API connections, respectively.

This configuration is automatically done by the action ```install_node``` or can be done by the action ```setup_node```

#### Automatic startup
* The script sets up a cron job to automatically start the Quilibrium node whenever the system reboots. This ensures your node is always running unless manually stopped.

#### Notes
By using the install_node action, you can streamline the Quilibrium node installation process, saving you time and effort.

### Backing up node configuration ```backup_node```

The ```backup_node``` action provides a convenient way to create local backups of your Quilibrium node configuration files. This is essential for disaster recovery purposes and allows you to restore your node's settings if necessary.

#### What gets backed up

* The script retrieves the following critical configuration files from each target node:
  * ```config.yml```: This file stores core configuration settings for your Quilibrium node.
  * ```keys.yml```: This file contains sensitive security keys used by your node. 

#### Backup location

The script stores the backed-up files in a directory named ```./backup``` within your current working directory.
Each node's backup files are placed in a separate subfolder named after the node's hostname, ensuring clear organization and identification.

### Monitor your Quilibrium node ```install_watchdog```

This optional feature provides real-time monitoring of your Quilibrium node and the ability to receive notifications via Telegram. It can be a valuable tool for staying informed about your node's health.

#### Functionality

* The ```install_watchdog``` command sets up a monitoring service on the target node.
* The service continuously checks for potential issues with your node's operation.
* If an issue is detected, the following actions occur (configurable):
  - **Automatic Restart:** The node can be automatically restarted to potentially resolve the issue.
  - **Telegram Notification:** An alert message is sent to your Telegram chat, notifying you of the problem.

#### Using the Watchdog installer

* Execute the following command to install the watchdog on the target node:
```
./qtools.sh install_watchdog <target> telegram_id=<telegram_chat_id> auto_restart=<auto_restart> telegram_level=<level>
```
Where:

* ```target```: the hostname of the node you want to monitor.
* ```telegram_id=<telegram_chat_id>```: your Telegram chat ID (see instructions below).
* ```auto_restart=<auto_restart>```: set to ```true``` to automatically restart the node on issues, or ```false``` to only receive notifications.
* ```telegram_level=<level>```: Choose ```all``` to receive notifications for all events, or none to disable notifications.

#### Important note about telegram
* To find your Telegram chat ID, follow these steps:
  * Open your Telegram app.
  * In the search bar, type "**userinfobot**".
  * Select the contact named "**userinfobot**".
  * Tap "**Start**" at the bottom of the chat window.
  * The bot will reply with your User ID (the chat ID).

* **<span style="color:red">MANDATORY:</span>** Initiate a chat with the Quilibrium bot:
  * Search for "@Quilibrium_bot" in Telegram
  * Send it a message (e.g., "hello").

#### Watchdog commands

Find here different commands to manage your node once connected into:

* To start service, run
```
sudo systemctl start quilibrium_watchdog
```

* To stop service, run
```
sudo systemctl stop quilibrium_watchdog
```

* To restart service, run
```
sudo systemctl restart quilibrium_watchdog
```

* To view service logs run
```
sudo journalctl -u quilibrium_watchdog -f
```

## Examples

To restart all your nodes
```
./qtools.sh restart_node all
```
To restart nodes from the "quilibrium" group defined in your inventory:
```
./qtools.sh restart_node quilibrium
```
To restart a single node name "node01":
```
./qtools.sh restart_node node01
```

## Defining Your Nodes (Inventory)

Quilibrium Tools rely on an inventory file located at [inventories/hosts.yml](inventories/hosts.yml) to define your nodes and their details. This file serves as a blueprint for Ansible to identify and manage your nodes.<br/>
Here's an example of a basic inventory structure:

```
nodes:
  vars:
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

* This example defines a group called "nodes" containing three individual nodes named node01, node02, and node03.
* Each node entry specifies its hostname (ansible_host) for connection purposes.
* The ansible_user variable defines the username used for SSH access to the nodes.
* The ansible_password variable is crucial, but we'll address how to secure it in the next section.
* Refer to the Ansible documentation for more information on inventories: https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html

### Important notes
Variables are defined into the file [inventories/group_vars/all.yml](inventories/group_vars/all)
* You can change the default user ```ansible_user``` (ubuntu by default)
* You can change the root path of the Quilibrium node

## Securing Passwords with Ansible Vault

Ansible Vault provides a robust solution for encrypting sensitive information like node passwords within your project. This ensures your credentials remain secure, even if your code repository is exposed. Here's a detailed guide on utilizing Ansible Vault:

1. **Create a vault file:**
* Open a terminal and navigate to your project directory.
* Run the following command to create a new vault file named vaults/vault.yml
```
ansible-vault create vaults/vault.yml
```
This command initializes an empty vault file encrypted with a randomly generated key.<br/>

2. **Adding Passwords to the Vault:**

* Use the following command to edit the vault file:
```
ansible-vault edit vaults/vault.yml
```

This will open your default text editor (usually Vim or Nano) with the vault file content.
* Inside the editor, add your passwords as key-value pairs. For example, to store your Quilibrium node password:

```
quilibrium_password: "<your_strong_password>"
```

**Important:** replace <your_strong_password> with your password.

* Save and close the editor. The passwords are now securely encrypted within the vault file.

3. **Referencing Passwords from Inventory:**

* Update your ```inventories/hosts.yml``` file to reference the password from the vault. Modify the ansible_password variable like this:

```
nodes:
  vars:
    ansible_password: '{{ quilibrium_password }}'  # Reference from vault
  hosts:
    # ... (Your node definitions)
```

4. **Managing the Vault File:**

* To edit the vault and update passwords:

```
ansible-vault edit vaults/vault.yml
```

* To view the contents of the vault file in a decrypted format:

```
ansible-vault view vaults/vault.yml
```

## Additional Security Best Practices:

* **Limit Vault Access:** Restrict access to the vault file itself. Consider storing it outside your version control system (e.g., Git) to prevent accidental exposure.
* **Regular Password Rotation:** Implement a regular password rotation schedule for your node passwords and update them within the vault accordingly.
* **Vault Password Management:** Choose a strong password for the vault itself and consider using a password manager to store it securely.

By following these steps and best practices, you can effectively secure your node passwords within the Quilibrium Tools project, enhancing the overall security posture of your Quilibrium node management.

## Node commands

Find here different commands to manage your node once connected into:

* To start service, run
```
sudo systemctl start quilibrium
```

* To stop service, run
```
sudo systemctl stop quilibrium
```

* To restart service, run
```
sudo systemctl restart quilibrium
```

* To view service logs run
```
sudo journalctl -u quilibrium -f
```