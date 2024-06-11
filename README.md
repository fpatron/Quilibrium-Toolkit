# Quilibrium Tools: Manage your Nodes with ease

This project provides a toolkit for simplifying the management of your Quilibrium nodes.<br/>
With these tools, you can perform essential actions and monitor multiple nodes effortlessly, saving you valuable time and ensuring smooth operation.<br/>
https://source.quilibrium.com/quilibrium/ceremonyclient.git

<img src="https://quilibrium.com/logo.png" width="50%" />

## Overview

* **Centralized Management:** manage multiple Quilibrium nodes from a single location, eliminating the need to interact with each node individually.
* **Simplified Actions:** perform common tasks like installation, backup, retrieval of information and rewards, starting/stopping/rebooting nodes with a single command.
* **Flexibility:** group your nodes for targeted management or manage them all at once.
* **Security:** leverage Ansible's robust features to manage passwords securely using Ansible Vault (explained in detail later).
* **Built with Ansible:** This toolkit utilizes the power of Ansible, a popular open-source automation tool, for efficient node management (https://github.com/ansible/ansible).

## Quick start

* Configure ```inventories/hosts.yml```
  - More details [here](docs/inventory.md)
* Configure ```inventories/group_vars/all.yml```
  - More details [here](docs/inventory.md)
* Launch the toolkit 
  - More details [here](#ssHowToUseIt)


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




## How to use it? <a id='ssHowToUseIt'></a>

The tools are provided as a script named ```qtools.sh```. To use it, follow this syntax:

```
./qtools.sh <command> <target>
```


* \<command\>: this defines the operation you want to perform on the target node(s).
* ```<target>```: this specifies the node(s) you want to target. It can be:
  * ```all```: Applies the action to all nodes defined in your ```inventory``` file.
  * A group name defined in your inventory (e.g., ```quilibrium```).
  * The hostname of a specific node (e.g., ```node01```).

## Commands details

### Node commands

| Command | Description |
| ---   | --- |
install_node | Installs a new Quilibrium node on the specified target(s).<br>[See install and configure guide](docs/installation.md)
install_tools | Install a little tool to check node info on the node directly.<br>[See install and configure guide](docs/installation.md)
upgrade_node | Upgrade Quilibrium node on the specified target(s).<br>[See install and configure guide](docs/installation.md)
setup_node | Configure sysctl and Quilibrium API (config.yml) on the specified target(s).<br>[See install and configure guide](docs/installation.md)
create_service | Install your Quilibrium node as a service (daemon) on the specified target(s).<br>[See install and configure guide](docs/installation.md)
fastsync_node | Sync your node with the latest snapshot. If you are having difficulties with synchronization, you can use this task to install the latest snapshot store folder on the specified target(s).<br>[See fastsync guide](docs/fastsync.md)
backup_node | Creates a backup of Quilibrium configuration files on the target node(s) and saves them locally in the ```./backup``` folder.<br>[See backup guide](docs/backup.md)
restore_node | Restore a backup of Quilibrium configuration files on the target node(s).<br>[See backup guide](docs/backup.md)
get_node_info | Retrieves information about the Quilibrium node(s), such as its current max_frame, peer id...<br>[See node info guide](docs/info.md)
get_node_reward | Fetches information about the rewards earned by the Quilibrium node(s).<br>[See node info guide](docs/info.md)
start_node | Starts the Quilibrium node(s) on the specified target(s)..
stop_node | Stops the Quilibrium node(s) running on the specified target(s)..
restart_node | Restarts the Quilibrium node(s) on the specified target(s)..
reboot_node | Reboots the specified target(s)..

### Grafana commands

| Command | Description |
| ---   | --- |
install_grafana | Supervise your node(s) with grafana and get all information about it

[See "Supervise your node" guide for more information](docs/grafana.md)


### Watchdog commands

| Command | Description |
| ---   | --- |
install_watchdog | Monitor your node(s) and get notify about its/their status.
start_watchdog | Start watchdog service on the specified target(s).
stop_watchdog | Stop watchdog service on the specified target(s).
restart_watchdog | Restart watchdog service on the specified target(s).

[See "Monitor your node" guide for more information](docs/watchdog.md)

## Defining your nodes (inventory)

[See "Defining your nodes" guide for more information](docs/inventory.md)

## Secure your nodes

[See "Secure your nodes" guide for more information](docs/vault.md)

## Migrate your existing nodes

[See "How to migrate your existing node(s)" guide for more information](docs/migration.md)

## Docs

* [How to install and configure your node(s)?](docs/installation.md)
* [How to define your nodes inventory?](docs/inventory.md)
* [How to secure your node(s)?](docs/vault.md)
* [How to fastsync your node(s)?](docs/fastsync.md)
* [How to backup your node(s)?](docs/backup.md)
* [How to get info about your node(s)?](docs/info.md)
* [How to monitor your node(s)?](docs/watchdog.md)
* [How to migrate existing node(s)?](docs/migration.md)
