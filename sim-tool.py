#!/usr/bin/env python

import getopt
import sys
from sim import Sms
from sim import Gps
from sim import Lte
from sim import Output


tool = ""
file = ""
port = "/dev/ttyS0"  # Raspberry Pi 3
verbose = False
action = ""
apn = ""
status = Sms.SmsStatus.UNREAD
location1 = ""
location2 = ""


def version():
    version_file = sys.path[0]+"/version"
    with open(version_file, 'r') as fin:
        print(fin.read())


def usage():
    print("usage sim-tool [tool] [options]")
    print("Tools:")
    print("sms          : Tools for SMS")
    print("gps          : Tools for GPS")
    print("lte          : Tools for LTE/data")
    print("Options:")
    print("-f --file    : Write output json to specified file")
    print("-p --port    : Device to use, default /dev/ttyS0")
    print("-v --verbose : Activate verbose logging to console")
    print("-h --help    : Print this text")
    print("   --version : Print the version number")
    print("")


def usage_sms():
    print("usage sim-tool sms -a [action] [options]")
    print("Actions:")
    print("read             : Read SMS")
    print("delete           : Delete SMS")
    print("Options:")
    print("-f --file        : Write sms json to specified output file")
    print("-p --port        : Device to use, default /dev/ttyS0")
    print("-v --verbose     : Activate verbose logging to console")
    print("-h --help        : Print this text")
    print("Special action options:")
    print("--status          : SMS status (READ,UNREAD,ALL) for action read")
    print("Example:")
    print("sim-tool sms -a delete")
    print("sim-tool sms --action=read --status=ALL --file=lte.json --verbose")
    print("")


def usage_gps():
    print("usage sim-tool gps -a [action] [options]")
    print("Actions:")
    print("read             : Read GPS location")
    print("distance         : Calculate distance between locations")
    print("Options:")
    print("-f --file        : Write gps json to specified output file")
    print("-p --port        : Device to use, default /dev/ttyS0")
    print("-v --verbose     : Activate verbose logging to console")
    print("-h --help        : Print this text")
    print("Special action options:")
    print("--location1      : Location 1 as JSON for action distance")
    print("--location2      : Location 2 as JSON for action distance")
    print("Example:")
    print("sim-tool gps")
    print("sim-tool gps --action=distance --location1={\"latitude\": 51.83609516666667, \"longitude\": 7.40293035} --location2={\"latitude\": 51.4589493434, \"longitude\": 7.3434}")
    print("")

def usage_lte():
    print("usage sim-tool lte -a [action] [options]")
    print("Actions:")
    print("activate-device  : Activate device")
    print("activate-raw-ip  : Activate raw_ip for network interface")
    print("activate-network : Activate network")
    print("activate-dhcp    : Activate DHCP and get an IP")
    print("mode             : Check device mode")
    print("signal           : Check signal strength")
    print("network          : Check home network")
    print("interface        : Check the interface name")
    print("Options:")
    print("-f --file        : Write output json to specified file")
    print("-p --port        : Device to use, default /dev/ttyS0")
    print("-v --verbose     : Activate verbose logging to console")
    print("-h --help        : Print this text")
    print("Special action options:")
    print("--apn            : Set APN for action activate-network")
    print("Example:")
    print("sim-tool lte -a activate-device")
    print("sim-tool lte --action=activate-network --apn=pinternet.interkom.de --file=lte.json --verbose")
    print("")


if __name__ == "__main__":
    try:
        tool = sys.argv[1]
        if tool == "--version":
            version()
            sys.exit(2)
        if tool == "--help":
            usage()
            sys.exit(2)
        if tool not in ['sms', 'gps', 'lte']:
            print("Tool '" + tool + "' is invalid. Please run sim-tool --help for more information.")
            sys.exit(2)
        opts, args = getopt.getopt(sys.argv[2:], 't:f:p:a:hv', ['tool=', 'file=', 'port=', 'help', 'verbose', 'action=',
                                                                'apn=', 'status=', 'location1=', 'location2='])
    except (getopt.GetoptError, IndexError) as e:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-f', '--file'):
            file = arg
        elif opt in ('-p', '--port'):
            port = arg
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-a', '--action'):
            action = arg
        elif opt == '--apn':
            apn = arg
        elif opt == '--status':
            if arg == "READ":
                status = Sms.SmsStatus.READ
            elif arg == "UNREAD":
                status = Sms.SmsStatus.UNREAD
            elif arg == "ALL":
                status = Sms.SmsStatus.ALL
            else:
                usage_sms()
                sys.exit(2)
        elif opt == '--location1':
            location1 = arg
        elif opt == '--location2':
            location2 = arg
        else:
            usage()
            sys.exit(2)

    out = Output(file, verbose)
    if tool == "sms":
        if action == "read":
            sms = Sms(port, out)
            sms.print_read_sms(status)
            sms.close()
        elif action == "delete":
            sms = Sms(port, out)
            sms.print_delete_sms()
            sms.close()
        else:
            usage_sms()
            sys.exit(2)

    elif tool == "gps":
        if action == "read" or action == "":
            gps = Gps(port, out)
            gps.print_location()
            gps.close()
        elif action == "distance":
            Gps.action_distance(location1, location2)
        else:
            usage_gps()
            sys.exit(2)

    elif tool == "lte":
        lte = Lte(out)
        if action == "activate-device":
            lte.action_activate_device()
        elif action == "activate-network":
            if apn == "":
                usage_lte()
                sys.exit(2)
            lte.action_activate_network(apn)
        elif action == "activate-raw-ip":
            lte.action_activate_raw_ip()
        elif action == "activate-dhcp":
            lte.action_activate_dhcp()
        elif action == "mode":
            lte.action_check_mode()
        elif action == "signal":
            lte.check_signal()
        elif action == "network":
            lte.action_check_network()
        elif action == "interface":
            lte.action_check_interface()
        else:
            usage_lte()
            sys.exit(2)
    else:
        usage()
        sys.exit(2)
