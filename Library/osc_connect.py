import socket
import time
import sys
import paho.mqtt.client as mqtt



TEK =  [["*CLS\r\n", "*WAI\r\n"], [ "MEASUREMENT:MEAS1:VALUE?\r\n", "MEASUREMENT:MEAS2:VALUE?\r\n"]]

TEK_HOST = '192.168.1.121'
TEK_PORT = 4000
SERVER_FAILED = False
SERVER_OK = True
BUFFER_SIZE = 1024

class Osscilscope:

    def __init__(self):
        self.socket = None
        # self.measure_clear_errors()


    def connect_measure(self, host, port):
        if self.socket:
            self.close_measurement()
            self.status = SERVER_FAILED
            return SERVER_FAILED
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except OSError as msg:
            self.socket = None
            self.status = SERVER_FAILED
            return SERVER_FAILED
        try:
            self.socket.connect((host, port))
            self.socket.settimeout(2.0)
            try:
                self.socket.recv(1024)
            except:
                pass
            self.socket.settimeout(None)
        except OSError as msg:
            self.close_measurement()
            return SERVER_FAILED
        time.sleep(1)
        return True


    def measure_frequency(self):
            time.sleep(1)
            err = self.measure_send(b'CLEAR\r\n')
            if err == SERVER_FAILED:
                self.status = SERVER_FAILED
                return SERVER_FAILED, None
            time.sleep(2)
            err = self.measure_send(b'MEASUREMENT:MEAS1:VALUE?\r\n')
            if err == SERVER_FAILED:
                self.status = SERVER_FAILED
                return SERVER_FAILED, None
            time.sleep(1)
            err, data1 = self.measure_receive()
            err = self.measure_send(b'MEASUREMENT:MEAS2:VALUE?\r\n')
            if err == SERVER_FAILED:
                self.status = SERVER_FAILED
                return SERVER_FAILED, None
            time.sleep(1)
            err, data2 = self.measure_receive()
            try:
                d1 = data1.decode('ascii').strip().replace('>', '').replace('\r', '').replace('\n', '').replace('fetc?', '').replace(',+ Over', '').replace('   ', '').replace(' ',',')
                d2 = data2.decode('ascii').strip().replace('>', '').replace('\r', '').replace('\n', '').replace('fetc?', '').replace(',+ Over', '').replace('   ', '').replace(' ',',')
            except UnicodeDecodeError:
                ...
                # return DECODING_ERROR, None
            # if not d1 or not d2:
            #     return DECODING_ERROR, None
            # r1 = d1[0:(fErrMsg.find('\\'))]
            # r2 = d2[0:(fErrMsg.find('\\'))]
            # # print(r1, r2)
            # try:
            #     r1 = float(d1)
            #     r2 = float(d2)
            # except ValueError:
            #     return DECODING_ERROR, None
            return SERVER_OK, data1, data2

    def measure_send(self, text):
        self.socket.sendall(text)

    def measure_receive(self):

        data = self.socket.recv(BUFFER_SIZE)
        err = False
        return err, data




osc = Osscilscope()
osc.connect_measure(TEK_HOST,TEK_PORT)
tek_data = osc.measure_frequency()

...