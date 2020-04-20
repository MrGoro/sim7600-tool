#!/bin/bash

# Check LTE module operating mode

sudo qmicli -d /dev/cdc-wdm0 --dms-get-operating-mode

# output:
#
# offline:
#   [/dev/cdc-wdm0] Operating mode retrieved:
#	  Mode: 'low-power'
#	  Reason: 'unknown'
#	  HW restricted: 'no'
#
# online:
#   [/dev/cdc-wdm0] Operating mode retrieved:
#	  Mode: 'online'
#	  HW restricted: 'no'