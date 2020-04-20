#!/bin/bash

# Check network signal strength

sudo qmicli -d /dev/cdc-wdm0 --nas-get-signal-strength

# output
#
# [/dev/cdc-wdm0] Successfully got signal strength
# Current:
#	 Network 'lte': '-57 dBm'
# RSSI:
#	 Network 'lte': '-57 dBm'
# ECIO:
#	 Network 'lte': '-2.5 dBm'
# IO: '-106 dBm'
# SINR (8): '9.0 dB'
# RSRQ:
#	 Network 'lte': '-11 dB'
# SNR:
#	 Network 'lte': '6.4 dB'
# RSRP:
#	 Network 'lte': '-86 dBm'
