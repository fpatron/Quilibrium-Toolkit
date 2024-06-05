#!/bin/bash

# Display the commands the script can run
usage() {
    echo "Usage: $0 {start|stop|restart|journal|frame|dif}"
    echo "quil start   : The script will start the quilibrium node"
    echo "quil stop    : The script will stop the quilibrium node"
    echo "quil restart : The script will restart the quilibrium node"
    echo "quil journal : The script will display quilibrium logs"
    echo "quil frame   : The script will display frame number"
    echo "quil dif     : The script will display current difficulty"
    exit 1
}

# if no argument is passed, script will display quilibrium logs
if [ -z "$1" ]; then
    journalctl -u quilibrium -f
    exit 0
fi

# "frame" : The script will display frame number
case "$1" in
    frame)
        journalctl -u quilibrium -n 100 -f | stdbuf -oL grep "current_frame" | while read -r line; do 
            echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; 
            echo " $(echo "$line" | grep -o '"current_frame":[0-9]\+')"; 
        done
        ;;
# "dif" : The script will display current difficulty
    dif)
        journalctl -u quilibrium -n 100 -f | stdbuf -oL grep "next_difficulty_metric" | while read -r line; do 
            echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; 
            echo " $(echo "$line" | grep -o '"next_difficulty_metric":[0-9]\+')"; 
        done
        ;;
# "start" : The script will start the quilibrium node
    start)
        sudo systemctl start quilibrium
        ;;
# "stop" : The script will stop the quilibrium node
    stop)
        sudo systemctl stop quilibrium
        ;;
# "restart" : The script will restart the quilibrium node
    restart)
        sudo systemctl restart quilibrium
        ;;
# "journal" : The script will display quilibrium logs
    journal)
        journalctl -u quilibrium -f
        ;;
    *)
        usage
        ;;
esac
