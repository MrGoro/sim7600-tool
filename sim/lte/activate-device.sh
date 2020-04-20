#!/bin/bash

# Activate LTE module

sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'
