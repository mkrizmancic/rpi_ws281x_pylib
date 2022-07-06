#!/bin/bash


trap 'killall' INT

killall() {
    trap '' INT TERM     # ignore INT and TERM while shutting down
    echo "**** Shutting down... ****"     # added double quotes
    sudo kill -TERM 0         # fixed order, send TERM not INT
    wait
    echo DONE
    exit
}

sudo LED_server &
sleep 2
python3 $1.py

cat
