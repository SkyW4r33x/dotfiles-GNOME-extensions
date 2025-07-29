#!/bin/sh

# Get IP address using ip command
ip="$(ip -4 addr show eth0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')"

if [ -n "${ip}" ]; then
    echo "󰈁 $ip"
else
    echo "󰈁 Sin Internet"
fi

