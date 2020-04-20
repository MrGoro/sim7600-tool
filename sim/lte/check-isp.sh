#!/bin/bash

# Check current isp and ip

IP=$(curl -s https://ipinfo.io/ip)
ISP=$(curl -s "https://www.whoismyisp.org/ip/$IP" | grep -oP -m1 '(?<=isp">).*(?=</p)')

echo "ISP: $ISP"
echo "IP:  $IP"
