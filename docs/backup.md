# Backing up node configuration ```backup_node```

The ```backup_node``` command provides a convenient way to create local backups of your Quilibrium node configuration files. This is essential for disaster recovery purposes and allows you to restore your node's settings if necessary.

<img src="https://staticfiles.acronis.com/images/blog-cover/696aba821d856b6e452815b12e98d97b.png" width="50%" />

### How?

* Execute the following command to backup your node(s)
```
./qtools.sh backup_node <target>
```

Where:
* ```<target>```: this specifies the node(s) you want to target. It can be:
  * ```all```: Applies the action to all nodes defined in your ```inventory``` file.
  * A group name defined in your inventory (e.g., ```quilibrium```).
  * The hostname of a specific node (e.g., ```node01```).

## What gets backed up

* The script retrieves the following critical configuration files from each target node:
  * ```config.yml```: This file stores core configuration settings for your Quilibrium node.
  * ```keys.yml```: This file contains sensitive security keys used by your node. 

## Backup location

The script stores the backed-up files in a directory named ```./backup``` within your current working directory.

Each node's backup files are placed in a separate subfolder named after the node's hostname, ensuring clear organization and identification.
