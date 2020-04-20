import time
import serial


class Sim:

    def __init__(self, port):
        self.modem = serial.Serial(port, 115200)

    def __send_command(self, command):
        self.modem.write(str.encode(command + "\r"))
        time.sleep(1)
        ret = []
        while self.modem.inWaiting() > 0:
            msg = self.modem.readline().strip().decode("UTF-8")
            msg = msg.replace("\r", "").replace("\n", "")
            if msg != "":
                ret.append(msg)
        return ret

    def ok(self):
        result = self.__send_command("AT")
        return len(result) == 2 and result[0] == 'AT' and result[1] == 'OK'

    def send_command(self, command):
        result = self.__send_command("AT+"+command)
        return result

    def close(self):
        self.modem.close()
