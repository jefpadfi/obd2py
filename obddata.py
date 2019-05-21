'''
Programmer: JR Padfield
Description: Pulls information from the obd 2 sensors.
Version: 1
Date: 07/15/2014

Most definitions were found in pi2go. Updated the equations according to OBDII PID wiki page.
'''

from config import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial
import config as conf

try:
    import serial
except ModuleNotFoundError:
    popup = Popup(title='pySerial Error',
                  content=Label(text='pySerial was not found on this machine. Please make sure to install it.'),
                  auto_dismiss=False)
    popup.open()


class ObdData(object):
    """Data collected from obd sensors """

    def __init__(self):
        self.serialIO = None

    def connectToSerial(self, dt):
        try:
            self.serialIO = serial.Serial(serialDevice, 38400, timeout=1)
            print("serialIO setup correctly")
            popup_serial = Popup(title='pySerial Setup',
                                 content=Label(text='pySerial has found the device. It will now work.'),
                                 size_hint=(None, None), size=(250, 150))
            popup_serial.open()
            Clock.schedule_interval(partial(self.readValues, OBDValues), .5)
        except NameError:
            popup_serial = Popup(title='pySerial Error',
                                 content=Label(text='pySerial is not installed. Please install it.'),
                                 size_hint=(None, None), size=(250, 150))
            popup_serial.open()
        except serial.serialutil.SerialException:
            popup_serial = Popup(title='Serial Device Error',
                                 content=Label(text='Serial device not found.'),
                                 size_hint=(None, None), size=(250, 150))
            popup_serial.open()
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
        # Check to make sure returned list is not empty
        if not speed_list:
            print("Speed is empty. Return 0")
            return 0
        if speed_list == -1 or speed_list == 0:
            print("There is an issue with reading the speed of the vehicle.")
            return 0
        else:
            speed_hex = speed_list[1]
            speed_float = float(int("0x" + speed_hex, 0))
            if speedFormat == "mph":
                # display speed in miles per hour
                speed_float *= 0.621371
            elif speedFormat == "kph":
                # display speed in kilometers per hour
                return speed_float
            else:
                # error
                print("Configuration is wrong. Please check config.py for speedFormat")
        return speed_float

    def rpm(self, oldValues):
        """ Gets the RPM of the engine """
        # TODO: Fix RPM display
        if self.serialIO is None:
            return "Serial IO not setup."
        self.serialWrite("0C")
        rpm_list = self.serialRead()
        # Check to make sure returned list is not empty
        if not rpm_list:
            print("RPM is empty. Return 0")
            return 0
        if rpm_list == -1:
            rpm_final = oldValues[1]
        else:
            rpm_hex1 = rpm_list[1]
            rpm_hex2 = rpm_list[2]
            rpm_list[0] = float(int("0x" + rpm_hex1, 0))
            rpm_list[1] = float(int("0x" + rpm_hex2, 0))

            # Calculate the actual rpm
            rpm_final = ((rpm_list[0] * 256) + rpm_list[1]) / 4
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
        # Check to make sure returned list is not empty
        if not temp_list:
            print("Intake Temp is empty. Return 0")
            return 0
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
        # Check to make sure returned list is not empty
        if not temp_list:
            print("Oil Temp is empty. Return 0")
            return 0
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
        # Check to make sure returned list is not empty
        if not temp_list:
            print("Coolant Temp is empty. Return 0")
            return 0
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
        # Check to make sure returned list is not empty
        if not load_list:
            print("Engine Load is empty. Return 0")
            return 0
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
        # Check to make sure returned list is not empty
        if not temp_list:
            print("Air Flow Rate is empty. Return 0")
            return 0
        if temp_list == -1:
            return oldValues[6]
        else:
            # find the actual value.
            temp_hex = temp_list[1]
            temp_list = float(int("0x" + str(temp_hex), 0))
            flow_rate = ((temp_list * 256) + temp_list) / 100

        return flow_rate

    def mpg(self, oldValues):
        """ Returns the MPG for the car. """
        return 710.7 * oldValues[0] / oldValues[6]

    def readValues(self, OBDvalues, dt):
        """ Gets all the values to display! """
        if self.serialIO is not None:
            conf.updateText.ids.speed.text = ObdData.speed(self, OBDvalues)
            conf.updateText.ids.rpm.text = ObdData.rpm(self, OBDvalues)
            conf.updateText.ids.instake_tmep.text = ObdData.intake_temp(self, OBDvalues)
            # conf.updateText.ids.oil_temp.text = obddata.oil_temp(self, OBDvalues)
            conf.updateText.ids.coolant_temp.text = ObdData.coolant_temp(self, OBDvalues)
            conf.updateText.ids.engine_load.text = ObdData.engine_load(self, OBDvalues)
            # OBDValues[6] = obddata.air_flow_rate(self, OBDvalues)
            # OBDValues[7] = obddata.mpg(self, OBDvalues)

