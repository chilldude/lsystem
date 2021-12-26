from os import listdir
import re
import serial

DEVICE_PATTERN = 'cu.usbserial*'
BAUD = 9600


class Plotter:
    def __init__(self):
        self.device = serial.Serial(self.find_device_name(), BAUD)
        print(self.device.name)

    def setup(self):
        self.initialize_plotter()
 
    def initialize_plotter(self):
        self.device.write(b'IN;')

    def pa(self, x, y):
        self.device.write('PA{},{};'.format(x,y).encode())

    def pd(self):
        self.device.write(b'PD;')

    def pu(self):
        self.device.write(b'PU;') 

    def sp(self, n):
        if 0 < n <= 6:
            self.device.write('SP{};'.format(n).encode())
        else:
            raise PlotterException("Invalid pen")

    def find_device_name(self):
        device_dir = '/dev/'
        filtered_values = list(filter(lambda v: re.match(DEVICE_PATTERN, v), listdir(device_dir)))
        if len(filtered_values) != 1:
            raise PlotterException("Device not found")

        return device_dir + filtered_values[0]

    def prepare_hpgl(self, body, buflen=40):
        start = [b"IN;PU;"]
        end = [b"SP0;"]
        final = start + body + end

        # read in 20 bytes at a time or boundary
        count = 0
        buf = []
        for ins in final:
            if count + len(ins) >= buflen:
                yield b"".join(buf)
                buf = []
                count = len(ins)
            else:
                count += len(ins)
            buf.append(ins)

        # send rest of the code
        yield b"".join(buf)

    def exec_hpgl(self, cmds):
        body = self.prepare_hpgl(cmds)
        for ins in body:
            print(ins)
            self.device.write(ins)

            # For every line sent, end with OA, which reports back current
            # position on the pen
            self.device.write(b"OA;")
            c = b""
            data = b""
            while c != b'\r':
                c = self.device.read()
                data += c
                print("read: {}".format(c))
            print("OA return: {}".format(data))
            # We got data, mean OA got executed, so the instruction buffer
            # is all consumed, ready to sent more.


class PlotterException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Plotter Exception"
