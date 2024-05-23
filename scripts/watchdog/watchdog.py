import socket
import requests
import json
import logging
import re
from datetime import datetime
import subprocess
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

# Restart automatically node
AUTO_RESTART= os.getenv("AUTO_RESTART", 'False').lower() in ('true', '1', 't') or False

# Threshold for frame duration in seconds
FRAME_DURATION_THRESHOLD = os.getenv("FRAME_DURATION_THRESHOLD") or 4500

# Telegram bot token and chat ID
TELEGRAM_PUBLISH_LEVEL = os.getenv("TELEGRAM_PUBLISH_LEVEL") or "all"
TELEGRAM_BOT_TOKEN = '6787115559:AAFbfCTM8Q0YelI3WHniWnjkJU6M7zVvf-k'
TELEGRAM_USER_ID= os.getenv("TELEGRAM_USER_ID") or None

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def getNodeLogs():
    """
    Fetch logs from the quilibrium service using journalctl.
    """
    cmd = 'journalctl -u quilibrium --since "2 hour ago" --no-pager | tac'
    try:
        logger.debug("Executing command to fetch logs")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        result.check_returncode()
        logger.debug("Logs fetched successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to fetch logs: {e}")
        return None

def formatTimestamp(ts):
    """
    Convert a Unix timestamp to a human-readable date.
    """
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')

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
    result = {
        "current_head_frame": {
            "value": None,
            "date": None,
            "timestamp": None
        },
        "uncooperative_peers": {
            "value": None,
            "date": None,
            "timestamp": None
        },
        "my_balance": {
            "value": None,
            "date": None,
            "timestamp": None
        },
        "lobby_state": {
            "value": None,
            "date": None,
            "timestamp": None
        }
    }

    for log in logs:
        if result["current_head_frame"]["value"] is None and "current_head_frame" in log:
            result["current_head_frame"]["value"] = log["current_head_frame"]
            result["current_head_frame"]["date"] = formatTimestamp(log["ts"])
            result["current_head_frame"]["timestamp"] = log["ts"]
        
        if result["uncooperative_peers"]["value"] is None and "uncooperative_peers" in log:
            result["uncooperative_peers"]["value"] = log["uncooperative_peers"]
            result["uncooperative_peers"]["date"] = formatTimestamp(log["ts"])
            result["uncooperative_peers"]["timestamp"] = log["ts"]
        
        if result["my_balance"]["value"] is None and "my_balance" in log:
            result["my_balance"]["value"] = log["my_balance"]
            result["my_balance"]["date"] = formatTimestamp(log["ts"])
            result["my_balance"]["timestamp"] = log["ts"]
        
        if result["lobby_state"]["value"] is None and "lobby_state" in log:
            result["lobby_state"]["value"] = log["lobby_state"]
            result["lobby_state"]["date"] = formatTimestamp(log["ts"])
            result["lobby_state"]["timestamp"] = log["ts"]

    logger.debug(f"Processed data: {result}")
    return result

def notifyUser(data):
    if (TELEGRAM_PUBLISH_LEVEL is not None and TELEGRAM_PUBLISH_LEVEL == 'all'):
        message = f"Balance: {data['my_balance']['value'] or 0}\n"
        message += f"Current head frame: {data['current_head_frame']['value'] or 0}\n"
        message += f"Uncooperative peers: {data['uncooperative_peers']['value'] or 0}\n"
        message += f"Lobby state: {data['lobby_state']['value'] or 'NA'}"
        publishToTelegram(message)

def publishToTelegram(message):
    """
    Publish a message to a Telegram chat.
    """
    try:
        if (TELEGRAM_USER_ID is not None):
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            data = {
                'chat_id': TELEGRAM_USER_ID,
                'text': f"<b>[{socket.gethostname()}]</b>\n{message}",
                'parse_mode': 'html'
            }
            res = requests.post(url, json = data)
            if (res.status_code == 200):
                logger.info("Message sent to Telegram successfully")
            else:
                logger.error("Message not sent to Telegram")
    except Exception as e:
        logger.error(f"Failed to send message to Telegram: {e}")

def needRestartNode(data):
    """
    Determine if the node needs to be restarted based on the logs data.
    """
    needRestart = False
    
    if data is not None:
        if data["uncooperative_peers"]["value"] is None:
            logger.warning("Node not ready, uncooperative_peers data missing")
        elif data["current_head_frame"]["timestamp"] is not None:
            duration = (datetime.now() - datetime.fromtimestamp(data["current_head_frame"]["timestamp"])).total_seconds()
            logger.debug(f"Time since last head frame: {duration} seconds")
            needRestart = duration > FRAME_DURATION_THRESHOLD

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
        publishToTelegram("Node is DOWN!\nIt has been automatically restarted")
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
            publishToTelegram("Node is not running!")
            return False
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check node status: {e}")
        return False

def main():
    """
    Main function to check quilibrium node logs and take appropriate actions.
    """
    logger.info("Starting quilibrium node checking")
    
    if not isNodeRunning():
        logger.warning("Node is not running")
        restartNode()
        exit(1)
    
    output = getNodeLogs()

    if output is None:
        logger.error("Failed to fetch logs")
        exit(1)

    logs = formatToJson(output)
    if logs is None:
        logger.error("Failed to parse logs as JSON")
        exit(1)

    data = processLogs(logs)
    
    if data is not None:
        notifyUser(data)
    
        if needRestartNode(data):
            logger.warning("Node restart required")
            if (AUTO_RESTART):
                restartNode()
            else:
                publishToTelegram("Node is DOWN!\nA restart is required")
        else:
            logger.info("Node is running fine")

if __name__ == "__main__":
    main()
