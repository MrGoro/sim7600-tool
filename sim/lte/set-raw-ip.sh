#!/bin/bash

# Set the network interface to raw_ip

INTERFACE=$(sudo qmicli -d /dev/cdc-wdm0 -w)
STATE=$(cat "/sys/class/net/$INTERFACE/qmi/raw_ip")

echo "Changing interface $INTERFACE type raw_ip from $STATE to Y"

sudo ip link set "$INTERFACE" down
echo 'Y' | sudo tee "/sys/class/net/$INTERFACE/qmi/raw_ip"
sudo ip link set "$INTERFACE" up
