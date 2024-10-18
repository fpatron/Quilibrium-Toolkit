# Install and Configure Your Quilibrium Node

The `install_node` command automates the process of setting up a new Quilibrium node on your target(s).

Here are the details of what it does:

## Installation Directory
* By default, Quilibrium will be installed in the following directory:
```
/home/<your user>/quilibrium
```
* You can change it by updating the variable `node_path` in the file `inventory/group_var/all.yml` ([see dedicated guide](inventory.yml)).

## Additional Packages
* The script automatically installs any necessary additional packages required for Quilibrium to run correctly.

## System Configuration Updates
* The script modifies the system configuration file `/etc/sysctl.conf` to include the following parameters:
```
net.core.rmem_max=7500000
net.core.wmem_max=7500000
```
These parameters adjust the network buffer sizes to potentially improve Quilibrium's performance.


## Quilibrium configuration
* The script set up the Quilibrium configuration file (```node/.config/config.yml```). It sets the following parameters within the configuration file:
```
listenMultiaddr: /ip4/0.0.0.0/udp/8336/quic-v1
statsMultiaddr: "/dns/stats.quilibrium.com/tcp/443"
listenGrpcMultiaddr: /ip4/127.0.0.1/tcp/8337
listenRESTMultiaddr: /ip4/127.0.0.1/tcp/8338
```
* listenMultiaddr: this parameter defines the peer UDP port
* statsMultiaddr: this parameter defines the address where the node will send statistics.
* listenGrpcMultiaddr and listenRESTMultiaddr: these parameters specify the IP addresses and ports on which the node listens for incoming GRPC and REST API connections, respectively.

This configuration is automatically done by the action ```install_node``` or can be done by the action ```setup_node```

You have the possibility to override the default ports of your hosts using this variables:
listenMultiaddr: /ip4/0.0.0.0/udp/8336/quic-v1
* `quilibrium_udp_port`: it will override the default port 8336 for the parameter `listenMultiaddr`
* `quilibrium_grpc_port`: it will override the default port 8337 for the parameter `listenGrpcMultiaddr`
* `quilibrium_rest_port`: it will override the default port 8338 for the parameter `listenRESTMultiaddr`

This configuration is automatically done by the action `install_node` or can be done by the action `setup_node`.

## Upgrade your node(s)

* Execute the following command to upgrade your node(s)
```
./qtools.sh upgrade_node <target>
```

This command will:
* stop your node
* fetch latest Quilibrium version
* build your node
* start your node

## Automatic Startup
* The script adds a service to automatically start the Quilibrium node whenever the system reboots. This ensures your node is always running unless manually stopped.

### Useful Commands

Find here different commands to manage your node once connected:

* To start the service, run:
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

### Note

You can install the Quilibrium service individually by using the command `create_service`.



## Tools Addons

The `install_tools` command install a little tool on the node. 

It will allow you to check some informations directly on the node, and stop, start, restart the node.

To use it on node, simply run the command, no matter what directory you are in:

* Watch the logs :
```
quil
```
or
```
quil journal
```

* Start the node :
```
quil start
```

* Stop the node :
```
quil stop
```

* Restart the node :
```
quil restart
```

*  View node current frame
```
quil frame
```

* View node difficulty
```
quil dif
```
