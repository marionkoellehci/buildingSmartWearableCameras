#!/usr/bin/env bash
export DISPLAY=:0.0
cd /home/pi/smartcameras
echo $(pwd)
if [[ $(sudo ./toggle.sh | grep '[t]urned off') ]]; then
  sudo ./toggle.sh
fi
cd modules
nohup sudo -E ./eye_servo.py > /dev/null 2>&1 &
