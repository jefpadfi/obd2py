'''
Programmer: JR Padfield
Description: Launches the program
Version: 1
Date: 07/15/2014
'''

from tkinter import *
from config import guiUpdate
import gui



class OBD2PY(Frame):
    def __init__(self, master):
        """ Loads all files and executes the gui """
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