'''
Programmer: JR Padfield
Description: Configuration for the obd data
Version: 1
Date: 07/15/2014
'''

# Location for the serial device to communicate to
serialDevice = ''

# Degrees format
degreeFormat = "f"  # f = fahrenheit c = celsius

# Speed format
speedFormat = "mph"  # mph = us format, kph = metric format

# fuel mileage
fuelFormat = "mpg"  # mpg = miles per gallon, lpg = liters per gallon

# logging
logging = True  # if you want to use SQLite to log the information set it to true.
                # If you don't want to log it set to false.