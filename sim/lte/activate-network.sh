#!/bin/bash

# Activate mobile network

sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='$1',ip-type=4" --client-no-release-cid
