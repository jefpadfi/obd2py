'''
Programmer: JR Padfield
Description: Launches the program
Version: 1
Date: 07/15/2014
'''

from tkinter import *
from config import guiUpdate, serialDevice
import gui
from obddata import obddata

try:
    import serial
except AttributeError:
    print("Please install pySerial so we can use this program")



class OBD2PY(Frame):
    def __init__(self, master):
        """ Loads all files and executes the gui """
        obddata.__init__(self)
        super(OBD2PY, self).__init__(master)
        self.grid()
        gui.GUI.create_gui(self)
        self.run()

    def run(self):
        """ Runs the main program and updates values """
        gui.GUI.update_gui(self)
        self.after(guiUpdate, self.run)

if __name__ == "__main__":
    ''' Start the application '''
    root = Tk()
    root.title("OBD2PY - By: The Doctor")
    root.geometry("320x240")
    app = OBD2PY(root)
    root.mainloop()