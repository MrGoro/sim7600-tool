#!/bin/bash

# Get the home network information

sudo qmicli -d /dev/cdc-wdm0 --nas-get-home-network

# output
#
# [/dev/cdc-wdm0] Successfully got home network:
#	Home network:
#		MCC: '262'
#		MNC: '7'
#		Description: 'o2 - de'
