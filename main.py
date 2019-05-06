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

try:
    import serial
except AttributeError:
    print("Please install pySerial so we can use this program")


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
        return MainScreen()


if __name__ == "__main__":
    """ Run the kivy app """
    ObdiiPy().run()
