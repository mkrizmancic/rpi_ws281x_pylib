#!/bin/bash

# robot_name="$(rosparam get /robot_name)_"
# number_of_nodes=$(rosparam get /num_of_robots)
# debug="$(rosparam get /debug_kalman)"

# echo "Launching $number_of_nodes Kalman filter nodes..."

trap 'killall' INT

killall() {
    trap '' INT TERM     # ignore INT and TERM while shutting down
    echo "**** Shutting down... ****"     # added double quotes
    sudo kill -TERM 0         # fixed order, send TERM not INT
    wait
    echo DONE
}

sudo python3 LED_server.py &
sleep 2
python3 LED_client.py &

cat
