#!/bin/bash

if [[ $(hostname) == "rog-g14" ]]; then
    /home/sohfix/programs/sysix/sys_ops/stream/bin/python3.11 "$@"
elif [[ $(hostname) == "sohfix-imac" ]]; then
    /home/sohfix/programs/development/stream/bin/python3.12 "$@"
else
    echo "Unknown machine!"
    exit 1
fi
