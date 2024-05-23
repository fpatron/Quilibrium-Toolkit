# Sync your nodes quickly

The synchronization process for Quilibrium nodes often takes a long time, sometimes several days.

<img src="https://cdn-icons-png.flaticon.com/512/6378/6378038.png" width="30%" />

However, it's possible to bypass this process by fetching a snapshot provided by [CherryServers](https://www.cherryservers.com/?affiliate=676XHODW).

So, if you're experiencing difficulties with synchronization, you can use the job to synchronize your node(s) with the latest data:

```
./qtools.sh fastsync <target>
```

Where:
* ```<target>```: this specifies the node(s) you want to target. It can be:
  * ```all```: Applies the action to all nodes defined in your ```inventory``` file.
  * A group name defined in your inventory (e.g., ```quilibrium```).
  * The hostname of a specific node (e.g., ```node01```).
