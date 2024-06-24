
# Monitor your node(s)

This optional feature provides real-time monitoring of your Quilibrium node and the ability to receive notifications via Telegram or Discord. It is a valuable tool for staying informed about your node's health.

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
./qtools.sh install_watchdog <target>
```
Add these variables into your var files (see [inventories/group_vars/all.example.yml](../inventories/group_vars/all.example.yml) for an example):

* ```watchdog_timer```: define period to execute the watchdog in minutes (default is 60)
* ```watchdog_auto_restart: <auto_restart>```: (optional) set to ```true``` to automatically restart the node on issues, or ```false``` to only receive notifications.
* ```watchdog_telegram_id: <telegram_chat_id>```: (optional) your Telegram chat ID (see instructions below).
* ```watchdog_discord_webhook: <discord_webhook>```: (optional) your Discord webhook url (see instructions below).
* ```watchdog_publish_level: <level>```: (optional) choose ```all``` to receive notifications for all events, or none to disable notifications.
* ```watchdog_restart_on_memory_leak: <level>```: (optional) choose ```true``` to restart automatically your node in case of memory leak (only available for version 1.4.20-p0).

## Notes about Telegram 

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

## Notes about Discord 

<img src="https://upload.wikimedia.org/wikipedia/fr/thumb/4/4f/Discord_Logo_sans_texte.svg/213px-Discord_Logo_sans_texte.svg.png" width="50"/>

* Create a new channel in your Discord server
* In the settings of your channel, go to the menu `Integrations`
* Create a new webhook and copy the URL
* This URL will be used by the parameter `discord_webhook`

## Watchdog commands

| Command | Description |
| ---   | --- |
install_watchdog | Monitor your node(s) and get notify about its/their status.
start_watchdog | Start watchdog service on the specified target(s).
stop_watchdog | Stop watchdog service on the specified target(s).

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