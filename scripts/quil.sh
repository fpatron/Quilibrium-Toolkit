#!/bin/bash

# Fonction pour afficher l'utilisation du script
usage() {
    echo "Usage: $0 {start|stop|restart|journal}"
    exit 1
}

# Si aucun argument n'est fourni, lancez le journal par défaut
if [ -z "$1" ]; then
    journalctl -u quilibrium -f
    exit 0
fi

# Exécuter la commande appropriée en fonction de l'argument fourni
case "$1" in
    frame)
        # avec le nom de la machine
        # journalctl -u quilibrium -n 100 | grep "current_frame" | while read line; do echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; echo " $(echo "$line" | grep -o '"current_frame":[0-9]\+')" ; done
        journalctl -u quilibrium -n 100 | grep "current_frame" | while read line; do echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; echo " $(echo "$line" | grep -o '"current_frame":[0-9]\+')" ; done
        
        journalctl -u quilibrium -f | stdbuf -oL grep "current_frame" | while read -r line; do 
#            echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; 
            echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; 
                echo " $(echo "$line" | grep -o '"current_frame":[0-9]\+')"; 
        done
        ;;
    dif)
        journalctl -u quilibrium -n 100 | grep "next_difficulty_metric" | while read line; do echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; echo " $(echo "$line" | grep -o '"next_difficulty_metric":[0-9]\+')" ; done
        journalctl -u quilibrium -f | stdbuf -oL grep "next_difficulty_metric" | while read -r line; do 
            echo "$line" | grep -o '^[^ ]\+ \+[^ ]\+ \+[^ ]\+' | tr -d '\n'; 
            echo " $(echo "$line" | grep -o '"next_difficulty_metric":[0-9]\+')"; 
        done
        ;;
    start)
        systemctl start quilibrium
        ;;
    stop)
        systemctl stop quilibrium
        ;;
    restart)
        systemctl restart quilibrium
        ;;
    journal)
        journalctl -u quilibrium -f
        ;;
    *)
        usage
        ;;
esac
