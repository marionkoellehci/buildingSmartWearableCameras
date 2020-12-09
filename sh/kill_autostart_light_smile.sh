#!/usr/bin/env bash

if [[ $(ps -ef | grep '[s]udo -E ./test_light_smile.py') ]]; then
    sudo kill $(ps -ef | grep '[s]udo -E ./test_light_smile.py' | tr -s ' ' | cut -d ' ' -f 2)
    echo "killed off"
else
  echo "nothing to kill"
fi
