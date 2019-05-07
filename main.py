"""
Programmer: JR Padfield
Description: Launches the program
Version: 2
Date: 07/15/2014
Date Edited: 05/06/2019
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from settings_json import settings_json
from obddata import ObdData
from kivy.clock import Clock
from log import ObdLogging


obdii_setting = None
obdii = ObdData()
obdlogging = ObdLogging()
obdlogging.check_for_db()

Clock.schedule_once(obdii.connectToSerial, 2)


class MainScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


# Let's load GUI File for the app
presentation = Builder.load_file('gui.kv')


class ObdiiPy(App):
    title = "OBD2PY - By: The Crzy Doctor"

    def build(self):
        """ Builds the gui and returns the gui object to display. """
        self.use_kivy_settings = False
        global obdii_setting
        obdii_setting = self.config.items('obdii_settings')
        return MainScreen()

    def build_config(self, config):
        config.setdefaults('obdii_settings', {
            'use_mph': 1,
            'use_fahrenheit': 1,
            'enable_logging': 1
        })

    def build_settings(self, settings):
        settings.add_json_panel('OBD2PY Settings',
                                self.config,
                                data=settings_json)


if __name__ == "__main__":
    """ Run the kivy app """
    ObdiiPy().run()
