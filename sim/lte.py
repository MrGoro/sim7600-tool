import json
import re
from subprocess import Popen, PIPE
from .output import Output


def shell(command):
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"")
    rc = p.returncode
    return {'out': output, 'error': err, 'rc': rc}


class Lte:

    def __init__(self, out=Output()):
        self.out = out
        self.interface = self.check_interface()

    def action_activate_device(self):
        result = self.activate_device()
        if result:
            self.out.verbose("Device activated")
        else:
            self.out.verbose("Device not activated")
        json_result = {'activated': result}
        self.out.output(json.dumps(json_result))
        return json_result

    def activate_device(self):
        self.out.verbose("Activating Device")

        result = shell(["bash", "./sim/lte/activate-device.sh"])
        self.out.verbose(result['out'])

        return result['rc'] == 0 and result['out'].strip() == '[/dev/cdc-wdm0] Operating mode set successfully'

    def action_activate_network(self, apn):
        result = self.activate_network(apn)
        self.out.output(json.dumps({'activateNetwork': {'successful': result}}))

    def activate_network(self, apn):
        self.out.verbose("Activating mobile network for APN " + apn)

        result = shell(["bash", "./sim/lte/activate-network.sh", apn])
        self.out.verbose(result['out'])

        return result['rc'] == 0

    def action_activate_dhcp(self):
        result = self.activate_dhcp()
        self.out.output(json.dumps({'activateDhcp': {'successful': result}}))

    def activate_dhcp(self):
        self.out.verbose("Activating DHCP")

        result = shell(["bash", "./sim/lte/activate-dhcp.sh"])
        self.out.verbose(result['out'])

        return result['rc'] == 0

    def action_check_mode(self):
        result = self.check_mode()
        active = result == 'online'
        json_status = {'status': {'active': active, "mode": result}}
        self.out.output(json.dumps(json_status))
        return json_status

    def check_mode(self):
        self.out.verbose("Check Operation mode")

        result = shell(["bash", "./sim/lte/check-mode.sh"])
        self.out.verbose(result['out'])

        result_offline = 'offline'
        if result['rc'] != 0:
            return result_offline

        # https://regex101.com/r/r3V2Fi/1
        regex = r"\[\/dev\/.*\] Operating mode retrieved:\n\sMode: '(?P<mode>.*)'\n\sHW restricted: '(?P<hwrestricted>.*)'"
        matches = re.findall(regex, result['out'], re.MULTILINE)
        if not matches:
            return result_offline

        match = matches[0]
        return match[0]

    def check_signal(self):
        self.out.verbose("Check Signal Strength")

        result = shell(["bash", "./sim/lte/check-signal.sh"])
        self.out.verbose(result['out'])
        # TODO Implement JSON response

    def action_check_network(self):
        result = self.check_network()
        network_json = json.dumps(result)
        self.out.output(network_json)

    def check_network(self):
        self.out.verbose("Check Home Network")

        result = shell(["bash", "./sim/lte/check-home-network.sh"])
        self.out.verbose(result['out'])

        # https://regex101.com/r/cmfRwH/2
        regex = r"\[\/dev\/.*\] Successfully got home network:\n\s+Home network:\n\s+MCC: '(?P<mcc>\d*)'\n\s+MNC: '(?P<mnc>\d*)'\n\s+Description: '(?P<network>.*)'"
        matches = re.findall(regex, result['out'], re.MULTILINE)
        if not matches:
            return {}

        match = matches[0]
        return {'mcc': int(match[0]), 'mnc': int(match[1]), 'network': match[2]}

    def action_check_interface(self):
        result = self.check_interface()
        json_interface = json.dumps({'interface': {'name': result}})
        self.out.output(json_interface)

    def check_interface(self):
        self.out.verbose("Check interface name")

        result = shell(["bash", "./sim/lte/check-interface.sh"])
        self.out.verbose(result['out'])

        if result['rc'] != 0:
            return ""
        return result['out'].strip()

    def action_activate_raw_ip(self):
        self.out.verbose("Activate raw_ip for network interface")

        result = shell(["bash", "./sim/lte/set-raw-ip.sh"])
        self.out.verbose(result['out'])

        return result['rc'] == 0
