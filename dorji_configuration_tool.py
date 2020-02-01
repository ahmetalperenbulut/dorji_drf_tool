#!/usr/bin/python3
# AhmetAlperenBULUT
# https://github.com/ahmetalperenbulut/dorji_drf_tool

import serial
import binascii
import os
from enum import Enum
import time


class Configuration_Values(Enum):
    FREQUENCY = 1
    RF_TRx_RATE = 2
    RF_POWER = 3
    BAUD_RATE = 4
    PARITY = 5
    WAKEUP_TIME = 6


class dorji_rf_module():
    def __init__(self):
        self._serial_port = None
        self._freq = 0
        self._freq_readable = 0
        self._rf_trx_rate = 0
        self._rf_power = 0
        self._baud_rate = 0
        self._parity = 0
        self._wakeup_time = 0
        self._connected = False
        self._READ_COMMAND = b'\xFF\x56\xAE\x35\xA9\x55\xF0'

    def connect(self, serialport, baudrate=9600, parity=serial.PARITY_NONE):
        try:
            self._serial_port = serial.Serial(port=serialport, baudrate=baudrate, bytesize=serial.EIGHTBITS,
                                              parity=parity, stopbits=serial.STOPBITS_ONE, timeout=0.1)
            self._connected = True

        except Exception as e:
            self._connected = False
            print(e)

    def disconnect(self):
        try:
            self._serial_port.close()
            self._connected = False

        except Exception as e:
            self._connected = False
            print(e)

    def _write_configurations(self):
        #data = b'\x24\x24\x24' + \
        data = b'\xFF\x56\xAE\x35\xA9\x55\x90' + \
            self._freq + self._rf_trx_rate+self._rf_power + \
            self._baud_rate+self._parity+self._wakeup_time
        
        print(binascii.hexlify(data))
        self._serial_port.write(data)
        time.sleep(0.2)
        response = self.read_data_from_serial()
        if response:
            self._parse_configurations(response)

    def read_configurations(self):
        if self._connected:
            self._serial_port.write(self._READ_COMMAND)
            configuration = self.read_data_from_serial()
            if configuration:
                self._parse_configurations(configuration)
                return True
        return False
    
    def read_data_from_serial(self):
        if self._connected:
            configuration = b''
            for val in iter(self._serial_port.read, b''):
                configuration = configuration + val
            return configuration
        return None
            
    def _mapping_readable_form(self, val, type):
        mapping = None
        if type == Configuration_Values.RF_TRx_RATE:
            convert_mapping = {0x00: 1, 0x01: 2,
                               0x02: 5, 0x03: 10, 0x04: 20, 0x05: 40}
            mapping = convert_mapping
        elif type == Configuration_Values.BAUD_RATE:
            convert_mapping = {0x00: 1200, 0x01: 2400, 0x02: 4800,
                               0x03: 9600, 0x04: 19200, 0x05: 38400, 0x06: 57600, 0x07: 115200}
            mapping = convert_mapping
        elif type == Configuration_Values.PARITY:
            convert_mapping = {0x00: "PARITY_NONE",
                               0x01: "PARITY_EVEN", 0x02: "PARITY_ODD"}
            mapping = convert_mapping
        elif type == Configuration_Values.WAKEUP_TIME:
            convert_mapping = {0x00: 0.05, 0x01: 0.1, 0x02: 0.2, 0x03: 0.4, 0x04: 0.6,
                               0x05: 1, 0x06: 1.5, 0x07: 2, 0x08: 2.5, 0x09: 3, 0x0a: 4, 0x0b: 5}
            mapping = convert_mapping

        return mapping[val]
    def _parse_configurations(self, configuration):
        print(binascii.hexlify(configuration))
        print("Module Type:", hex(configuration[1]))
        print("Module Version:", hex(configuration[2]))
        print("Frequency: {} KHz".format(
            ((configuration[3] << 16) | (configuration[4] << 8) | configuration[5])))
        self._freq = configuration[3] + configuration[4] + configuration[5]
        self._freq_readable = ((configuration[3] << 16) | (configuration[4] << 8) | configuration[5])

        print("TRx Rate: ", self._mapping_readable_form(
            configuration[6], Configuration_Values.RF_TRx_RATE))
        self._rf_trx_rate = configuration[6].to_bytes(1, 'big')
        print("RF Power(0-7):", configuration[7])
        self._rf_power = configuration[7].to_bytes(1, 'big')
        print("Baudrate(default:9600): {} bps".format(
            self._mapping_readable_form(configuration[8], Configuration_Values.BAUD_RATE)))
        self._baud_rate = configuration[8].to_bytes(1, 'big')
        print("Parity: {}" .format(self._mapping_readable_form(
            configuration[9], Configuration_Values.PARITY)))
        self._parity = configuration[9].to_bytes(1, 'big')
        print("WakeUp Time: {}" .format(self._mapping_readable_form(
            configuration[10], Configuration_Values.WAKEUP_TIME)))
        self._wakeup_time = configuration[10].to_bytes(1, 'big')

    def menu(self):
        while True:
            print("1-Frequency")
            print("2-TRx Rate")
            print("3-RF Power")
            print("4-Baudrate")
            print("5-Parity")
            print("6-WakeUp Time")
            val = int(input("Select value:"))
            if val == 1:
                self._freq = input("Frequency(418 ~ 455MHz)")
            elif val == 2:
                self._rf_trx_rate = input("TRx Rate(1, 2, 5,10, 20, 40)")
            elif val == 3:
                self._rf_power = input("RF Power(0 to 7)")
            elif val == 4:
                self._baud_rate = input(
                    "Baudrate(1200, 2400, 4800, 9600, 19200, 38400, 57600)")
            elif val == 5:
                self._parity = input(
                    "Parity(No parity(0), Even parity(1), Odd parity(2))")
            elif val == 6:
                self._wakeup_time = input(
                    "Wakeup Time(0.05, 0.1, 0.2, 0.4, 0.6, 1, 1.5, 2, 2.5, 3, 4, 5)")
            else:
                break


"""
rf = dorji_rf_module()

rf.connect("/dev/ttyUSB0")

rf.read_configurations()
rf.menu()
rf._write_configurations()
"""
