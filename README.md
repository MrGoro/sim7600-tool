# SIM7600 Tool
Command Line tool for basic communication with SIM7600E 4G &amp; GPS module

![Build Debian Package](https://github.com/MrGoro/sim7600-tool/workflows/Build%20Debian%20Package/badge.svg)

# Installation
The tool is currently not hosted on the official Debian repositories therefore you cannot install it with `apt-get install`.

First install dependencies:  
`sudo apt-get install`  

Download debian package from release section and install it by running:  
`sudo dpkg -i sim-tool_1.0.0-1_all.deb`

# Usage
For basic information about the usage type:  
`sim-tool --help` or just `sim-tool`

`sim-tool [tool] [options]`  

Tools  
```
sms           : Tools for SMS
gps           : Tools for GPS
lte           : Tools for LTE/data
```

Basic options used for all commands  
```
 -f --file    : Write output json to specified file
 -p --port    : Device to use, default /dev/ttyS0
 -v --verbose : Activate verbose logging to console
 -h --help    : Print usage information
    --version : Print the version number (no action)
```
_For tool specific options see sections below._

## SMS
sim-tool allows to read and delete SMS stored on the SIM7600 module.
To receive incoming SMS the module must be active (see LTE).

Read SMS (default state is "unread")  
`sim-tool sms -a read`

Read SMS in state "read"  
`sim-tool sms -a read --status=read`  

Read all SMS including read, unread and sent  
`sim-tool sms -a read --status=all`  

Delete all SMS  
`sim-tool sms -a delete`  


## GPS
sim-tool allows to read the current position of the module using its built-in GPS module. 
Position is returned as JSON of form:  
`{"altitude": 51.4, "longitude": 7.4029464166666665, "course": 124.0, "time": "2020-04-23T06:48:34.000Z", "latitude": 51.8361417, "speed": 0.0}`  

Get Position  
`sim-tool gps`  
_When reading the current position the GPS module is activated when inactive. 
Reading the position can take longer when the module is inactive.
When the module cannot get a position `{}` is returned._

Calculate difference of positions in m  
`sim-tool gps -a distance --location1="{\"latitude\": 51.83609516666667, \"longitude\": 7.40293035}" --location2="{\"latitude\": 51.4589493434, \"longitude\": 7.3434}"`

## LTE / 4G / Data
sim-tool supports setup of SIM7600 as a IP network interface in Linux. Futhermore it allows to read state information like home network or signal strength.

Activate device  
`sim-tool lte -a activate-device`  

Activate raw_ip for network interface  
`sim-tool lte -a activate-raw-ip`  

Activate network  
`sim-tool lte -a activate-network --apn=xxx.provider.com`  

Activate DHCP and get an IP  
`sim-tool lte -a activate-dhcp`  

Get operation mode  
`sim-tool lte -a mode`  

Get home network  
`sim-tool lte -a network`  

Get signal strength  
`sim-tool lte -a signal`  

Get the name of the Linux network interface  
`sim-tool lte -a interface`  
