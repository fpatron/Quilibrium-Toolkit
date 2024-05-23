
# Monitor your node(s)

This optional feature provides real-time monitoring of your Quilibrium node and the ability to receive notifications via Telegram. It is a valuable tool for staying informed about your node's health.

<img src="https://cdn-blog.adafruit.com/uploads/2013/01/WatchDog.png" />

## Install the Watchdog

* The ```install_watchdog``` command sets up a monitoring service on the target node(s).
* The service continuously checks for potential issues with your node's operation.
* If an issue is detected, the following actions occur (configurable):
  - **Automatic Restart:** The node can be automatically restarted to potentially resolve the issue.
  - **Telegram Notification:** An alert message is sent to your Telegram chat, notifying you of the problem.
* The watchdog is automatically **started** after the installation
* The watchdog monitors your **each hour**

### How?

* Execute the following command to install the watchdog on the target node:
```
./qtools.sh install_watchdog <target> telegram_id=<telegram_chat_id> auto_restart=<auto_restart> telegram_level=<level>
```
Where:

* ```target```: the hostname of the node(s) you want to monitor.
* ```telegram_id=<telegram_chat_id>```: your Telegram chat ID (see instructions below).
* ```auto_restart=<auto_restart>```: set to ```true``` to automatically restart the node on issues, or ```false``` to only receive notifications.
* ```telegram_level=<level>```: Choose ```all``` to receive notifications for all events, or none to disable notifications.

## Important note about telegram 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Telegram_2019_Logo.svg/240px-Telegram_2019_Logo.svg.png" width="50"/>


* To find your Telegram chat ID, follow these steps:
  * Open your Telegram app.
  * In the search bar, type "**userinfobot**".
  * Select the contact named "**userinfobot**".
  * Tap "**Start**" at the bottom of the chat window.
  * The bot will reply with your User ID (the chat ID).

* **<span style="color:red">MANDATORY:</span>** initiate a chat with the Quilibrium bot:
  * Search for "@Quilibrium_bot" in Telegram
  * Send it a message (e.g., "hello").

## Watchdog commands

| Command | Description |
| ---   | --- |
install_watchdog | Monitor your node(s) and get notify about its/their status.
start_watchdog | Start watchdog service on the specified target(s).
stop_watchdog | Stop watchdog service on the specified target(s).
restart_watchdog | Restart watchdog service on the specified target(s).

## Oneshot commands

Find here different commands to manage your watchdog once connected into your node:

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