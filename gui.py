'''
Programmer: JR Padfield
Description: Creates the entire gui and allows it to be updated
Version: 1
Date: 07/15/2014
'''
from tkinter import *
from tkinter import ttk


class GUI(object):
    """ Handles all gui for the program """
    def __init__(self, master):
        """ Initialize the root window of the program """
        # lets create a frame to hold out labels
        self.superframe = LabelFrame(master, padx=5, pady=5)
        self.superframe.grid(row=2, column=1)
        # create the notebook in master
        self.notebook = ttk.Notebook(self.superframe)
        self.notebook.grid(row=1, column=1)
        self.basicBook = ttk.Frame(self.notebook)
        self.advancedBook = ttk.Frame(self.notebook)
        self.notebook.add(self.basicBook, text="Basic Info")
        self.notebook.add(self.advancedBook, text="Advanced Info")

        # create a label
        self.mphLabel = Label(self.basicBook, text="0.0 MPH")
        self.mphLabel.grid(row=2, column=1)

        # TODO: create a book to set new settings that can be saved