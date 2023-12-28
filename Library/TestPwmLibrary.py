import time

import serial
from robot.api.deco import library, keyword
from osc_connect import Osscilscope

TEK = [["*CLS\r\n", "*WAI\r\n"], ["MEASUREMENT:MEAS1:VALUE?\r\n", "MEASUREMENT:MEAS2:VALUE?\r\n"]]

TEK_HOST = '192.168.1.121'
TEK_PORT = 4000
SERVER_FAILED = False
SERVER_OK = True
BUFFER_SIZE = 1024


@library
class TestPwmLibrary:
    def __init__(self):
        self.osc = Osscilscope()

        self.port = 'COM6'
        self.bandwidth = 9600

    @keyword
    def read_data(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        tek_data = self.osc.measure_frequency()
        if tek_data[0] == False:
            raise Exception("Error on read")

    @keyword
    def scenario_1(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'1')
        tek_data = self.osc.measure_frequency()
        if float(tek_data[1]) >= 4.1e6 or float(tek_data[1]) <= 3.9e6:
            raise Exception("Error on read")

    @keyword
    def scenario_h(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'h')
        # tek_data = self.osc.measure_frequency()
        # if tek_data[1] != 4:
        #     raise Exception("Error on read")

    @keyword
    def scenario_l(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'l')
        # tek_data = self.osc.measure_frequency()
        # if tek_data[1] != 4:
        #     raise Exception("Error on read")

    @keyword
    def scenario_2(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'2')
        tek_data = self.osc.measure_frequency()
        if float(tek_data[1]) >= 4.1e6/2 or float(tek_data[1]) <= 3.9e6/2:
            raise Exception("Error on read")

    @keyword
    def scenario_4(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'4')
        tek_data = self.osc.measure_frequency()
        if float(tek_data[1]) >= 4.1e6/4 or float(tek_data[1]) <= 3.9e6/4:
            raise Exception("Error on read")

    @keyword
    def scenario_8(self):
        self.osc.connect_measure(TEK_HOST, TEK_PORT)
        self.send_uart_data(r'8')
        tek_data = self.osc.measure_frequency()
        if float(tek_data[1]) >= 4.1e6/8 or float(tek_data[1]) <= 3.9e6/8:
            raise Exception("Error on read")

    def send_uart_data(self, data):
        # UART initialization
        ser = serial.Serial(self.port, self.bandwidth)
        ser.write(data.encode())  # Konwersja danych na bajty i wysłanie
        ser.close()


osc = Osscilscope()
osc.connect_measure(TEK_HOST, TEK_PORT)

# aa = TestPwmLibrary()
# aa.send_uart_data(r'1')
tek_data = osc.measure_frequency()

...
