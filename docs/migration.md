# How to Migrate an Existing Node?

It is possible to use this toolkit with your existing node(s) without starting from scratch.

## Before Migrating
1. Check that your `hosts.yml` file is well configured ([see guide](inventory.md)).
1. Check that your `vault.yml` file is well configured ([see guide](vault.md)).

## How to Proceed?

### 1. Set up the path of your Quilibrium node (optional)

We recommend having the same install path for all your nodes.
Instead of overriding the `node_path` variable, you can simply move your node into the default node path which is defined in the file `inventories/group_vars/all.yml`.
```
/home/<your user>/quilibrium
```
If you want to have a specific path for your existing node:
1. create a folder called `host_vars` into the directory `inventories`
2. create a file with the name of your node as defined in the `hosts.yml` file in the previous directory `host_vars` with the extension **.yml**
3. add a variable `node_path` into

Example for a node called `node_to_migrate`:

1. new file:  `inventories/host_vars/node_to_migrate.yml`
2. content of the file:

```
node_path: /Users/kandy/quilibrium
```

### 2. **Set up the login of your node**

The procedure is the same as above: just add a variable called `ansible_user`

Example for a node called `node_to_migrate`:

1. new file:  `inventories/host_vars/node_to_migrate.yml`
2. content of the file:

```
ansible_user: myuser
```

### 3. **Stop your node**

1. Connect to your remote machine
2. Stop your Quilibrium node as usual
3. Check that it is well stopped in the processes

* **<span style="color:red">IMPORTANT:</span>** remove all instructions you have to start your node automatically (in your crontab for example) or an existing service (`systemctl`)

### 4. **Create the Quilibrium service**

```
./qtools.sh create_service <target>
```
Where `<target>` is the target you migrate.

This command will create a service (`systemctl`).

See [Install and configure guide](installation.md) for more information

### 5. **Start your node**

```
./qtools.sh start_node <target>
```
Where `<target>` is the target you migrate.

### 6. **Install watchdog (optional)**

See [Monitor your node guide](watchdog.md) for more information.

## How to Verify Your Migration?

To test if your migration has been performed successfully, just launch this command and check if you get your peer ID.

* Execute the following command to upgrade your node(s)

```
./qtools.sh get_node_info <target>
```
Where `<target>` is the target you migrate.
