
# Supervise your node(s)

This optional feature provides real-time monitoring of your Quilibrium nodes using the power of Grafana.
See [https://github.com/fpatron/Quilibrium-Dashboard](https://github.com/fpatron/Quilibrium-Dashboard) for more details about the installation & configuration.

<img src="https://upload.wikimedia.org/wikipedia/commons/9/9d/Grafana_logo.png" />

## Install Grafana Alloy

* The ```install_grafana``` command sets up Grafana Alloy on the target node(s).

### How?

* Execute the following command to install Grafana Alloy on the target node:
```
./qtools.sh install_grafana <target>
```
Add these variables into your var files (see [inventories/group_vars/all.example.yml](../inventories/group_vars/all.example.yml) for an example):

* `graphana_prometheus_url`: url of your prometheus server
* `graphana_prometheus_username`: (optional) username to connect to prometheus server if it is secured
* `graphana_prometheus_password`: (optional) password to connect to prometheus server if it is secured
* `graphana_loki_url`: url of your loki server
* `graphana_loki_username`: (optional) username to connect to loki server if it is secured
* `graphana_loki_password`: (optional) password to connect to loki server if it is secured

## Configuration of Grafana Alloy

If needed, the configuration file of Alloy is here

```
/etc/alloy/config.alloy
```
