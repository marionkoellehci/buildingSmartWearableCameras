#!/bin/bash
# Created by Yannick Feld - January 2019
# disables screensaver or screen turning black by reseting the timer used for that every 20 seconds
#
# TL;DR    no black screen - no screensaver


while [ 1 ]
do
    xscreensaver-command -deactivate > /dev/null 2>&1
    sleep 20
done
