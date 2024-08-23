#!/bin/bash

if [[ $(hostname) == "rog-g14" ]]; then
    /home/sohfix/programs/sysix/sys_ops/stream/bin/python3.11 "$@"
    echo "worked"
elif [[ $(hostname) == "sohfix-imac" ]]; then
    /home/sohfix/PycharmProjects/sys_ops/.sysix/bin/python3.11 "$@"
    echo "worked"
else
    echo "Unknown machine!"
    exit 1
fi

################################################################
