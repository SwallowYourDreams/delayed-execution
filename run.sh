#!/bin/bash
sudo echo " "
cwd=$(dirname "$0")
nohup sudo python3 "$cwd/DelayedExecution.py" >/dev/null 2>&1 &
sleep 0.05
exit 0
