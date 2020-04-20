#!/bin/bash

# Get an IP from ISB with DHCP

INTERFACE=$(sudo qmicli -d /dev/cdc-wdm0 -w)
echo "Starting IP lease for interface $INTERFACE"

sudo udhcpc -i "$INTERFACE"
