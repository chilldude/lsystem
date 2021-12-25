from os import listdir
import re
import serial

DEVICE_PATTERN = 'cu.usbserial*'
BAUD = 9600


class Plotter:
    def __init__(self):
        self.device = serial.Serial(self.find_device_name(), BAUD)

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



class PlotterException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Plotter Exception"
