#!/bin/sh

if [ -f "$HOME/.config/bin/target/target.txt" ]; then
    read ip_address machine_name < "$HOME/.config/bin/target/target.txt"
    if [ -n "$ip_address" ] && [ -n "$machine_name" ]; then
        echo "󰓾  $ip_address - $machine_name"
    else
        echo "󰓾  Sin Objetivo"
    fi
else
    echo "󰓾  Sin Objetivo"
fi
