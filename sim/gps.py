import time
import re
import json
import datetime
import sys
from .sim import Sim
from .output import Output


class Gps:

    def __init__(self, port, out=Output()):
        self.sim = Sim(port)
        self.out = out
        if self.sim.ok():
            self.out.verbose("Successful init of GPS")
            if not self.check_status(2):
                print("Could not start GPS")
                sys.exit(2)

    def __parse_gps(self, input):
        # https://regex101.com/r/j2DHXO/1
        regex = r"\+CGPSINFO: (?P<lat>[\d.]+),(?P<latdir>[NS]),(?P<long>[\d.]+),(?P<longdir>[EW]),(?P<date>\d+),(?P<time>[\d.]+),(?P<alt>[\d.]+),(?P<speed>[\d.]+),(?P<course>[\d.]+)"
        matches = re.findall(regex, input, re.MULTILINE)
        if not matches:
            return {}
        else:
            match = matches[0]
            now = datetime.datetime.now()
            year = int(now.year / 100) * 100 + int(match[4][4:6])
            date = str(year) + '-' + match[4][2:4] + '-' + match[4][0:2]
            time = match[5][0:match[5].find('.')]
            time = time[0:2] + ':' + time[2:4] + ':' + time[4:6]
            timestamp = date + 'T' + time + '.000Z'
            gps = {'latitude': self.__convert_gps(match[0]), 'longitude': self.__convert_gps(match[2], match[3]),
                   'altitude': float(match[6]),
                   'speed': float(match[7]), 'course': float(match[8]), 'time': timestamp}
            return gps

    def __convert_gps(self, input, dir=''):
        pos = input.find('.') - 2
        degrees = input[0:pos]
        minutes = input[pos:]
        result = float(degrees) + (float(minutes) / 60)
        if dir == 'W':
            result = result * -1
        return result

    def check_status(self, retries=0):
        self.out.verbose("Check GPS status")
        gps_status = self.sim.send_command('CGPS?')
        if len(gps_status) != 3 and gps_status[1] != '+CGPS: 1,1':
            self.out.verbose("Activating GPS")
            gps_activate_result = self.sim.send_command('CGPS=1')
            self.out.verbose(gps_activate_result)
            time.sleep(5)
            if retries > 0:
                return self.check_status(retries - 1)
            else:
                return False
        else:
            self.out.verbose("GPS active")
        return True

    def get_location(self):
        gps_result = self.sim.send_command('CGPSINFO')
        if len(gps_result) != 3 and not gps_result[2] == 'OK':
            self.out.verbose("Error getting GPS data")
            return {}
        else:
            gps = self.__parse_gps(gps_result[1])
            return gps

    def print_location(self):
        gps = self.get_location()
        gps_json = json.dumps(gps)
        self.out.output(gps_json)

    def close(self):
        self.sim.close()


if __name__ == "__main__":
    port = "/dev/ttyS0"  # Raspberry Pi 3
    gps = Gps(port)
    gps.get_location()
    gps.close()
