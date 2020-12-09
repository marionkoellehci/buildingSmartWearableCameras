#!/bin/bash
# Created by Yannick Feld - January 2019
# script to toogle the disablesleep skript, which turns off the screensaver
#
# TL;DR   toggle disablesleep

if [[ $(ps -e | grep '[d]isablesleep.sh') ]]; then
    kill $(ps -e | grep '[d]isablesleep.sh' | tr -s ' ' | cut -d ' ' -f 2)
    echo "turned off"
else
    nohup ./disablesleep.sh > /dev/null 2>&1 &
    echo "turned on"
fi
