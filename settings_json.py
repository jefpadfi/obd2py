"""
Programmer: Jeffrey Padfield
Description: Application settings json list.
Date: 05/07/2019
Version: 1
"""

import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'OBDII Settings'},
    {'type': 'bool',
     'title': 'Use MPH',
     'desc': 'Use Miles Per Hour for speed.',
     'section': 'obdii_settings',
     'key': 'use_mph'},
    {'type': 'bool',
     'title': 'Use Fahrenheit',
     'desc': 'Use Fahrenheit for temperature.',
     'section': 'obdii_settings',
     'key': 'use_fahrenheit'},
    {'type': 'bool',
     'title': 'Enable Logging',
     'desc': 'Save trip information to a database.',
     'section': 'obdii_settings',
     'key': 'enable_logging'}
])