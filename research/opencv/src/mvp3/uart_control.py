import serial


class UartControl(object):
    def __init__(self):
        self._port = serial.Serial(
            "/dev/tty.usbserial-1410",
            baudrate=9600,
            timeout=1
        )
        out = self._port.read_until()
        print('Receiving...' + str(out))

    def set_speed(self, value):
        command = "speed=" + str(value) + "\n"
        self._port.write(command.encode("ascii"))
        out = self._port.read_until()
        print('Receiving...' + str(out))

    def start_step(self, value):
        command = "step=" + str(value) + "\n"
        self._port.write(command.encode("ascii"))
        out = self._port.read_until()
        print('Receiving...' + str(out))

    def enable_led(self, value):
        command = "led=" + str(value) + "\n"
        self._port.write(command.encode("ascii"))
        out = self._port.read_until()
        print('Receiving...' + str(out))

    def disable_led(self):
        self._port.write("led=0\n".encode("ascii"))
        out = self._port.read_until()
        print('Receiving...' + str(out))
