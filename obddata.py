'''
Programmer: JR Padfield
Description: Pulls information from the obd 2 sensors.
Version: 1
Date: 07/15/2014

Most definitions were found in pi2go. Updated the equations according to OBD-11PID wiki page.
'''

import string
import time
from config import *
try:
    import serial
except AttributeError:
    print("Please install pySerial so we can use this program")


class obddata(object):
    """Data collected from obd sensors """

    def __init__(self):
        try:
            self.serialIO = serial.Serial(serialDevice, 38400, timeout=1)
            print("serialIO setup correctly")
        except:
            print("Issue with communicating with the Serial device. "
                  "\nPlease check config.py's serialDevice setting is correct.")
            self.serialIO = None

    def serialWrite(self, cmd):
        """ Writes the command for info you want to grab. """
        self.serialIO.flushInput()
        self.serialIO.flushOutput()
        self.serialIO.write("01 " + cmd + " \r")

    def serialRead(self):
        """ Reads the output of obd """
        serialList = str(self.serialIO.readline()).split(' ')
        valueList = []

        for value in serialList:
            if value == ">01":
                return -1
            else:
                for char in value:
                    if char == '\r':
                        valueList.append(value[0:2])
                        return valueList[2:len(valueList)]
                valueList.append(value)
        return valueList[2:len(valueList)]

    def speed(self):
        """ Gets the speed of the vehicle """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0D")
        speed_list = self.serialRead()
        if speed_list == -1:
            print("There is an issue with reading the speed of the vehicle.")
            return 0
        speed_hex = speed_list[0]
        try:
            speed_float = float(int("0x"+speed_hex, 0))
        except:
            print("There is an issue with reading the speed of the vehicle.")
            return 0

        if speedFormat == "mph":
            # display speed in miles per hour
            speed_float *= 0.621371
        elif speedFormat == "kph":
            # display speed in kilometers per hour
            speed_float = speed_float
        else:
            # error
            print("Configuration is wrong. Please check config.py for speedFormat")

        return speed_float

    def rpm(self):
        """ Gets the RPM of the engine """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0C")
        rpm_list = self.serialRead()
        rpm_value = []
        rpm_value.append(rpm_list[0][4:6])
        rpm_value.append(rpm_list[0][6:8])
        try:
            rpm_value[0] = float(int("0x"+rpm_value[0], 0))
            rpm_value[1] = float(int("0x"+rpm_value[1], 0))
        except:
            # something went wrong
            print("There is an issue with reading the RPM of the vehicle")
            return 0

        # Calculate the actual rpm
        rpm_final = ((rpm_value[0]*256)+rpm_value[1])/4
        # return the correct rpm
        print(rpm_final)
        return rpm_final

    def intake_temp(self):
        # Gets the outside air temperature from the air intake
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0f")
        # write the values to a list
        temp_list = self.serialRead()
        temp_hex = temp_list[0][4:6]
        try:
            temp_float = float(int("0x"+temp_hex, 0))
        except:
            # error happened
            print("There is an issue with reading the temperature from air intake.")
            return 0

        temp_final = 0  # set temp_final to 0 in case something happens

        if degreeFormat == "f":
            # subtract 40 from the float to get celsius then convert to fahrenheit
            temp_final = temp_float - 40*(9/5)+32
        elif degreeFormat == "c":
            # subtract 40 from the float to get celsius
            temp_final = temp_float - 40
        else:
            # error
            print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def oil_temp(self):
        """ Gets the oil temperature of the vehicle """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("5C")
        # write the values to a list
        temp_list = self.serialRead()
        temp_hex = temp_list[0][4:6]
        try:
            temp_float = float(int("0x"+temp_hex, 0))
        except:
            # error happened
            print("There is an issue with reading the temperature from air intake.")
            return 0

        temp_final = 0  # set temp_final to 0 in case something happens

        if degreeFormat == "f":
            # subtract 40 from the float to get celsius then convert to fahrenheit
            temp_final = temp_float - 40*(9/5)+32
        elif degreeFormat == "c":
            # subtract 40 from the float to get celsius
            temp_final = temp_float - 40
        else:
            # error
            print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def coolant_temp(self):
        """ Gets the coolant temperature """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("05")
        # write the values to a list
        temp_list = self.serialRead()
        temp_hex = temp_list[0][4:6]
        try:
            temp_float = float(int("0x"+temp_hex, 0))
        except:
            # error happened
            print("There is an issue with reading the temperature from air intake.")
            return 0

        temp_final = 0  # set temp_final to 0 in case something happens

        if degreeFormat == "f":
            # subtract 40 from the float to get celsius then convert to fahrenheit
            temp_final = temp_float - 40*(9/5)+32
        elif degreeFormat == "c":
            # subtract 40 from the float to get celsius
            temp_final = temp_float - 40
        else:
            # error
            print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def engine_load(self):
        """ Gets the total load of the engine """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("04")
        load_list = self.serialRead()
        load_hex = load_list[0][4:6]
        try:
            load_float = float(int("0x"+load_hex, 0))
        except:
            print("There was an issue with reading the engine load")
            return 0

        load_final = (load_float*100)/255
        return load_final