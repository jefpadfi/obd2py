'''
Programmer: JR Padfield
Description: Configuration for the obd data
Version: 1
Date: 07/15/2014
'''

# Location for the serial device to communicate to
serialDevice = "COM3"

# Degrees format
degreeFormat = "f"  # f = fahrenheit c = celsius

# Speed format
speedFormat = "mph"  # mph = us format, kph = metric format

# fuel mileage
fuelFormat = "mpg"  # mpg = miles per gallon, lpg = liters per gallon

# logging
logging = True  # True = Log, False = no log

# List to hold values to display on lcd
OBDValues = [0, 0, 0, 0, 0, 0, 0, 0]
