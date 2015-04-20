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
        except():
            print("Issue with communicating with the Serial device. "
                  "\nPlease check config.py's serialDevice setting is correct.")
            self.serialIO = None

    def serialWrite(self, cmd):
        """ Writes the command for info you want to grab. """
        self.serialIO.flushInput()
        self.serialIO.flushOutput()
        code = "01 " + cmd + "\r"
        self.serialIO.write(code.encode())

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

    def speed(self, oldValues):
        """ Gets the speed of the vehicle """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0D")
        speed_list = self.serialRead()
        print("Contents of speed_list" + str(speed_list))
        if speed_list == -1 or speed_list == 0:
            print("There is an issue with reading the speed of the vehicle.")
            return 0
        else:
            speed_hex = speed_list[1]
            speed_float = float(int("0x" + speed_hex, 0))
            print("Speed float = " + str(speed_float))
            if speedFormat == "mph":
                # display speed in miles per hour
                speed_float *= 0.621371
                print("mph = " + str(speed_float))
            elif speedFormat == "kph":
                # display speed in kilometers per hour
                print("kph = " + str(speed_float))
                return speed_float
            else:
                # error
                print("Configuration is wrong. Please check config.py for speedFormat")
        return speed_float

    def rpm(self, oldValues):
        """ Gets the RPM of the engine """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0C")
        rpm_list = self.serialRead()
        if rpm_list == -1:
            rpm_final = oldValues[1]
        else:
            rpm_hex1 = rpm_list[0]
            rpm_hex2 = rpm_list[2]
            rpm_list[0] = float(int("0x" + rpm_list[0], 0))
            rpm_list[1] = float(int("0x" + rpm_list[1], 0))

            # Calculate the actual rpm
            #rpm_final = (rpm_list[0] * 256 + rpm_list[1]) / 4
            rpm_final1 = rpm_list[0] * 256 / 4
            rpm_final2 = rpm_list[1] * 256 / 4
            rpm_final = rpm_final1 + rpm_final2 - 744
            # return the correct rpm
            #print(rpm_final)

        return rpm_final

    def intake_temp(self, oldValues):
        # Gets the outside air temperature from the air intake
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0f")
        # write the values to a list
        temp_list = self.serialRead()
        if temp_list == -1:
            return oldValues[2]
        else:
            temp_hex = temp_list[0]
            temp_float = float(int("0x"+temp_hex, 0))

            temp_final = 0  # set temp_final to 0 in case something happens

            if degreeFormat == "f":
                # subtract 40 from the float to get celsius then convert to fahrenheit
                temp_final = temp_float * (9/5)+32
            elif degreeFormat == "c":
                # subtract 40 from the float to get celsius
                temp_final = temp_float - 40
            else:
                # error
                print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def oil_temp(self, oldValues):
        """ Gets the oil temperature of the vehicle """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("5C")
        # write the values to a list
        temp_list = self.serialRead()
        if temp_list == -1:
            return oldValues[3]

        else:
            temp_hex = temp_list[0]
            temp_float = float(int("0x"+temp_hex, 0))
            temp_final = 0  # set temp_final to 0 in case something happens

            if degreeFormat == "f":
                # subtract 40 from the float to get celsius then convert to fahrenheit
                temp_final = temp_float * (9/5)+32
            elif degreeFormat == "c":
                # subtract 40 from the float to get celsius
                temp_final = temp_float - 40
            else:
                # error
                print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def coolant_temp(self, oldValues):
        """ Gets the coolant temperature """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("05")
        # write the values to a list
        temp_list = self.serialRead()
        if temp_list == -1:
            return oldValues[4]
        else:
            temp_hex = temp_list[0]
            temp_float = float(int("0x"+ temp_hex, 0))

            temp_final = 0  # set temp_final to 0 in case something happens

            if degreeFormat == "f":
                # subtract 40 from the float to get celsius then convert to fahrenheit
                temp_final = temp_float * (9/5)+32
            elif degreeFormat == "c":
                # subtract 40 from the float to get celsius
                temp_final = temp_float - 40
            else:
                # error
                print("Configuration is wrong. Please check config.py for degreeFormat.")

        return temp_final

    def engine_load(self, oldValues):
        """ Gets the total load of the engine """
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("04")
        load_list = self.serialRead()
        if load_list == -1:
            return oldValues[5]
        else:
            load_hex = load_list[0]
            load_float = float(int("0x"+load_hex, 0))
            load_final = (load_float*100)/255
        return load_final

    def air_flow_rate(self, oldValues):
        """ Gets the MAF to help get the MPG """
        if self.serialIO is None:
            return "Serial IO not setup"
        self.serialWrite("10")
        temp_list = self.serialRead()
        if temp_list == -1:
            return oldValues[6]
        else:
            # find the actual value.
            temp_hex = temp_list
            temp_list = float(int("0x" + str(temp_hex), 0))
            flow_rate = ((temp_list * 256) + temp_list) / 100

        return flow_rate

    def mpg(self, oldValues):
        """ Returns the MPG for the car. """
        return 710.7 * oldValues[0] / oldValues[6]

    def readValues(self, OBDvalues):
        """ Gets all the values to display! """
        OBDValues[0] = obddata.speed(self, OBDvalues)
        OBDValues[1] = obddata.rpm(self, OBDvalues)
        OBDValues[2] = obddata.intake_temp(self, OBDvalues)
        #OBDValues[3] = obddata.oil_temp(self, OBDvalues)
        OBDValues[4] = obddata.coolant_temp(self, OBDvalues)
        OBDValues[5] = obddata.engine_load(self, OBDvalues)
        #OBDValues[6] = obddata.air_flow_rate(self, OBDvalues)
        #OBDValues[7] = obddata.mpg(self, OBDvalues)