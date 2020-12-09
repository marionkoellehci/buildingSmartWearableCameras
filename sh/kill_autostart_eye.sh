#!/usr/bin/env bash

if [[ $(ps -ef | grep '[s]udo -E ./eye_servo.py') ]]; then
    sudo kill $(ps -ef | grep '[s]udo -E ./eye_servo.py' | tr -s ' ' | cut -d ' ' -f 2)
    echo "killed off"
else
  echo "nothing to kill"
fi
