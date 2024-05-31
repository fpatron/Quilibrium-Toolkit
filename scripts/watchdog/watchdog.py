import socket
import requests
import json
import logging
import re
from datetime import datetime
import subprocess
import os
import psutil
from dotenv import load_dotenv # type: ignore

load_dotenv()

# Restart automatically node
AUTO_RESTART= os.getenv("AUTO_RESTART", 'False').lower() in ('true', '1', 't') or False

# Notifications
PUBLISH_LEVEL =  os.getenv("PUBLISH_LEVEL") or os.getenv("TELEGRAM_PUBLISH_LEVEL") or "all"
DISCORD_WEBHOOK_URL =  os.getenv("DISCORD_WEBHOOK_URL") or None
TELEGRAM_BOT_TOKEN = '6787115559:AAFbfCTM8Q0YelI3WHniWnjkJU6M7zVvf-k'
TELEGRAM_USER_ID= os.getenv("TELEGRAM_USER_ID") or None

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#
# Quilibrium methods
#

def needRestartNode(data):
    """
    Determine if the node needs to be restarted based on the logs data.
    """
    needRestart = False
    
    ## todo find limits to restart node

    return needRestart

def restartNode():
    """
    Restart the quilibrium node.
    """
    logger.debug("Restarting node...")
    try:
        cmd = 'systemctl restart quilibrium'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        result.check_returncode()
        publish("Node is DOWN!\nIt has been automatically restarted")
        logger.debug("Node successfully restarted")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart node: {e}")
        
def isNodeRunning():
    """
    Check status of quilibrium node.
    """
    logger.debug("Checking node status...")
    try:
        cmd = 'systemctl status quilibrium --no-pager'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            publish("Node is not running!")
            return False
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check node status: {e}")
        return False
    
def getNodeInfo():
    """
    Get node quilibrium information
    """
    logger.debug("Getting node information...")
    
    data = {
        "peer_id": "NA",
        "version": "NA",
        "max_frame": 0,
        "peer_score": 0,
        "owned_balance": 0,
        "unconfirmed_balance": 0,
        "difficulty": 0
    }
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = "./node -node-info"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=f"{current_dir}/../ceremonyclient/node")
        
        peer_id_match = re.search(r"Peer ID: (.+)", result.stdout)
        if peer_id_match:
            data["peer_id"] = peer_id_match.group(1)
            
        version_match = re.search(r"Version: (.+)", result.stdout)
        if version_match:
            data["version"] = version_match.group(1)
        
        max_frame_match = re.search(r"Max Frame: (\d+)", result.stdout)
        if max_frame_match:
            data["max_frame"] = int(max_frame_match.group(1))
        
        peer_score_match = re.search(r"Peer Score: (\d+)", result.stdout)
        if peer_score_match:
            data["peer_score"] = int(peer_score_match.group(1))
        
        owned_balance_match = re.search(r"Owned balance: (\d+) QUIL", result.stdout)
        if owned_balance_match:
            data["owned_balance"] = int(owned_balance_match.group(1))
        
        unconfirmed_balance_match = re.search(r"Unconfirmed balance: (\d+) QUIL", result.stdout)
        if unconfirmed_balance_match:
            data["unconfirmed_balance"] = int(unconfirmed_balance_match.group(1))

        data["difficulty"] = getDifficulty()
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get not information: {e}")
        
    return data

def getDifficulty():
    output = getNodeLogs()
    if output is None:
        logger.error("Failed to fetch logs")
        exit(1)
    logs = formatToJson(output)
    if logs is None:
        logger.error("Failed to parse logs as JSON")
        exit(1)
    data = processLogs(logs)
    return data['difficulty']
    

def getNodeLogs():
    """
    Fetch logs from the quilibrium service using journalctl.
    """
    cmd = 'journalctl -u quilibrium --since "1 hour ago" --no-pager | tac'
    try:
        logger.debug("Executing command to fetch logs")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        result.check_returncode()
        logger.debug("Logs fetched successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to fetch logs: {e}")
        return None

def formatToJson(output):
    """
    Parse log output and extract JSON objects.
    """
    json_logs = re.findall(r'({.*?})', output)
    try:
        logger.debug("Parsing logs to JSON")
        return [json.loads(log) for log in json_logs]
    except json.JSONDecodeError:
        logger.error("Failed to parse logs as JSON")
        return None

def processLogs(logs):
    """
    Process the logs and extract relevant information.
    """
    logger.debug("Processing logs")
    result = { "difficulty": None }

    for log in logs:
        if result["difficulty"] is None and "previous_difficulty_metric" in log:
            result["difficulty"] = log["previous_difficulty_metric"]

    logger.debug(f"Processed data: {result}")
    return result
    

#
# System stats methods
#

def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    total = disk_usage.total / (1024 ** 3)
    used = disk_usage.used / (1024 ** 3)
    free = disk_usage.free / (1024 ** 3)
    percent = disk_usage.percent
    return total, used, free, percent

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    sensors = psutil.sensors_temperatures()
    core_temperatures= sensors.get('coretemp')[0][1] if sensors is not None and sensors.get('coretemp') is not None else 0
    return cpu_usage, physical_cores, logical_cores, core_temperatures

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    total = memory_info.total / (1024 ** 3)
    available = memory_info.available / (1024 ** 3)
    used = memory_info.used / (1024 ** 3)
    percent = memory_info.percent
    return total, available, used, percent

#
# Messaging methods
#

def format_percentage(value, threshold=90):
    if value >= threshold:  # Assuming the limit is 100%, values above 90% should be highlighted
        return f"**{value}%** :red_circle:"
    return f"{value}%"

def formatDataForDiscord(data):
    node = data["node"]
    cpu = data["cpu"]
    disk = data["disk"]
    memory = data["memory"]
    
    embed = {
        "title": f"`  {socket.gethostname()}  `",
        "color": 0x3498db,
        "fields": [
            {
                "name": "Quilibrium node",
                "value": (
                    f"- Status: {'OK' if node is not None else 'KO'}\n"
                    f"- Version: {node['version']}\n"
                    f"- Max Frame: {node['max_frame']}\n"
                    f"- Difficulty: {node['difficulty']}\n"
                    f"- Peer Score: {node['peer_score']}\n"
                    f"- Owned balance: {node['owned_balance']}\n"
                    f"- Unconfirmed balance: {node['unconfirmed_balance']}"
                ),
                "inline": True
            },
            {
                "name": "CPU usage",
                "value": (
                    f"- Usage: {format_percentage(cpu['cpu_usage'], 90)}\n"
                    f"- Physical cores: {cpu['physical_cores']}\n"
                    f"- Logical cores: {cpu['logical_cores']}\n"
                    f"- Temperature: {cpu['core_temperatures']}°C"
                ),
                "inline": True
            },
            {
               "name": "\t",
               "value": "\t"
            },
            {
                "name": "Memory usage",
                "value": (
                    f"- Total Mmmory: {memory['total_memory']:.2f} GB\n"
                    f"- Available memory: {memory['available_memory']:.2f} GB\n"
                    f"- Used memory: {memory['used_memory']:.2f} GB\n"
                    f"- Memory usage: {format_percentage(memory['percent_memory'], 90)}"
                ),
                "inline": True
            },
            {
                "name": "Disk usage",
                "value": (
                    f"- Total disk: {disk['total_disk']:.2f} GB\n"
                    f"- Used disk: {disk['used_disk']:.2f} GB\n"
                    f"- Free disk: {disk['free_disk']:.2f} GB\n"
                    f"- Disk usage: {format_percentage(disk['percent_disk'], 90)}"
                ),
                "inline": True
            },
        ],
        "footer": {
            "text": f"Peer ID: {node['peer_id']}",
        }
    }
    
    return { "embeds": [embed] }

def formatDataForTelegram(data):
    node = data["node"]
    cpu = data["cpu"]
    disk = data["disk"]
    memory = data["memory"]
    
    message = (
        f"*Node information:*\n"
        f"- Status: {'OK' if node is not None else 'KO'}\n"
        f"- Peer ID: {node['peer_id']}\n"
        f"- Version: {node['version']}\n"
        f"- Max Frame: {node['max_frame']}\n"
        f"- Peer Score: {node['peer_score']}\n"
        f"- Owned balance: {node['owned_balance']}\n"
        f"- Unconfirmed balance: {node['unconfirmed_balance']}\n\n"
        f"*CPU usage:*\n"
        f"- Usage: {cpu['cpu_usage']}%\n"
        f"- Physical cores: {cpu['physical_cores']}\n"
        f"- Logical cores: {cpu['logical_cores']}\n"
        f"- Core temperatures: {cpu['core_temperatures']}°C\n\n"
        f"*Disk usage:*\n"
        f"- Total disk: {disk['total_disk']:.2f} GB\n"
        f"- Used disk: {disk['used_disk']:.2f} GB\n"
        f"- Free disk: {disk['free_disk']:.2f} GB\n"
        f"- Disk usage: {disk['percent_disk']}%\n\n"
        f"*Memory usage:*\n"
        f"- Total memory: {memory['total_memory']:.2f} GB\n"
        f"- Available memory: {memory['available_memory']:.2f} GB\n"
        f"- Used memory: {memory['used_memory']:.2f} GB\n"
        f"- Memory usage: {memory['percent_memory']}%"
    )
    
    return message

def notifyUser(data):
    publishToDiscord(formatDataForDiscord(data), None)
    publishToTelegram(formatDataForTelegram(data))

def publish(message):
    publishToTelegram(message)
    publishToDiscord(None, message)
    
def publishToDiscord(payload, message):
    """
    Publish a message to a discord channel.
    """
    try:
        if (DISCORD_WEBHOOK_URL is not None):
            url = DISCORD_WEBHOOK_URL
            data = payload or {
              "embeds": [{
                "title": f"`  Watchdog  `  {socket.gethostname()}",
                "description": message,
                "color": 3224376
              }]}
            res = requests.post(url, json = data)
            if (res.status_code >= 200 and res.status_code < 300):
                logger.info("Message sent to Discord successfully")
            else:
                logger.error("Message not sent to Discord")
    except Exception as e:
        logger.error(f"Failed to send message to Discord: {e}")
    

def publishToTelegram(message):
    """
    Publish a message to a Telegram chat.
    """
    try:
        if (TELEGRAM_USER_ID is not None):
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            data = {
                'chat_id': TELEGRAM_USER_ID,
                'text': (
                    f"*[{socket.gethostname()}]*"
                    f"\n\n"
                    f"{message}"
                ),
                'parse_mode': 'markdown'
            }
            res = requests.post(url, json = data)
            if (res.status_code == 200):
                logger.info("Message sent to Telegram successfully")
            else:
                logger.error("Message not sent to Telegram")
    except Exception as e:
        logger.error(f"Failed to send message to Telegram: {e}")

#
# Main
#

def main():
    """
    Main function to check quilibrium node logs and take appropriate actions.
    """
    logger.info("Starting quilibrium node checking")
    
    logger.info("=================================")
    logger.info(f"Auto restart is set to: {AUTO_RESTART}")
    if (TELEGRAM_USER_ID is None):
        logger.warning("Telegram ID is not setup, no message will be sent")
    else:
        logger.info(f"Telegram ID is set to: {TELEGRAM_USER_ID}")
    if (DISCORD_WEBHOOK_URL is None):
        logger.warning("Discord webhook url is not setup, no message will be sent")
    else:
        logger.info(f"Discord webhook url is set to: {DISCORD_WEBHOOK_URL}")
    logger.info(f"Publish info level is set to: {PUBLISH_LEVEL}")
    logger.info("=================================")
    
    if not isNodeRunning():
        logger.warning("Node is not running")
        restartNode()
        exit(1)
    
    info = getNodeInfo()
    total_disk, used_disk, free_disk, percent_disk = get_disk_usage()
    cpu_usage, physical_cores, logical_cores, core_temperatures = get_cpu_usage()
    total_memory, available_memory, used_memory, percent_memory = get_memory_usage()
    
    if info is not None:
        notifyUser({
            "node": info,
            "cpu": {
                "cpu_usage": cpu_usage,
                "physical_cores": physical_cores, 
                "logical_cores": logical_cores,
                "core_temperatures": core_temperatures,
            },
            "disk": {
                "total_disk": total_disk,
                "used_disk": used_disk,
                "free_disk": free_disk,
                "percent_disk": percent_disk,
            },
            "memory": {
                "total_memory": total_memory,
                "available_memory": available_memory,
                "used_memory": used_memory,
                "percent_memory": percent_memory,
            }
        })
    
        if needRestartNode(info):
            logger.warning("Node restart required")
            if (AUTO_RESTART):
                restartNode()
            else:
                publish("Node is DOWN!\nA restart is required")
        else:
            logger.info("Node is running fine")

if __name__ == "__main__":
    main()
