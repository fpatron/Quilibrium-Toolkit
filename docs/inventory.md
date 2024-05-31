# Defining your nodes in the inventory

Quilibrium Tools rely on an inventory file located at ```inventories/hosts.yml``` to define your nodes and their details.

<img src="https://t4.ftcdn.net/jpg/01/46/35/85/360_F_146358501_31AcLM4umtVDEpGfnLmvYHoAm7vTXkCR.jpg" width="50%" />

This file serves as a blueprint for Ansible to identify and manage your nodes.<br>
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
or [inventories/hosts.example.yml](../inventories/hosts.example.yml)

* This example defines a group called "```nodes```" containing three individual nodes named node01, node02, and node03.
* Each node entry specifies its hostname (ansible_host) for connection purposes.
* The ```ansible_password``` variable is crucial, but we'll address how to secure it in [this guide](vault.md).
* Refer to the Ansible documentation for more information on inventories: https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html

## Variables

#### Overview

Variables are defined in the file ```inventories/group_vars/all.yml```
* Use the file [inventories/group_vars/all.example.yml](../inventories/group_vars/all.yml) to create your file ```inventories/group_vars/all.yml```
* You can change the default user ```ansible_user``` (ubuntu by default)
* You can change the root path of the Quilibrium node ```node_path```
* The Quilibrium API ```quilibrium_api_url``` is reachable via the default value ```http://127.0.0.1:8338```. Change it if you change the default port in the ```config.yml``` file.
* ```ansible_become_pass``` is linked to your user password to connect as root on your nodes.

* Refer to the Ansible documentation for more information on variables: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html

```
ansible_user: fpa
node_path: /home/{{ ansible_user }}/quilibrium
ansible_become_pass: "{{ ansible_password }}"
quilibrium_api_url: "http://127.0.0.1:8338"
```

#### Groups

If you manage multiple groups with different user logins, you can create a YAML file named after the group in the folder ```group_vars```. Variables within will override variables in the ```all.yml``` file.
